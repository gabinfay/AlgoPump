#!/usr/bin/env python3
"""
Trading Bot SDK - Thin wrapper around existing pump-fun-bot functionality
This SDK provides a simplified interface to the existing, battle-tested trading infrastructure.
Now packaged as an MCP server for AI agents.
"""

import asyncio
import sys
import os
import base58
import struct
from typing import Optional, List, Callable, Dict, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# MCP Server imports
from fastmcp import FastMCP

# Solana imports for post-graduation trading
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.message import Message
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
from spl.token.instructions import (
    SyncNativeParams,
    create_idempotent_associated_token_account,
    get_associated_token_address,
    sync_native,
)

# Add the pump-fun-bot source to path  
PUMP_BOT_PATH = Path(__file__).parent / "pump-fun-bot"
PUMP_BOT_SRC_PATH = PUMP_BOT_PATH / "src"
if str(PUMP_BOT_PATH) not in sys.path:
    sys.path.insert(0, str(PUMP_BOT_PATH))
if str(PUMP_BOT_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(PUMP_BOT_SRC_PATH))

# Import existing components
from core.client import SolanaClient
from core.wallet import Wallet
from core.priority_fee.manager import PriorityFeeManager
from trading.platform_aware import PlatformAwareBuyer, PlatformAwareSeller
from trading.base import TradeResult as BaseTradeResult
from trading.position import Position as BasePosition
from monitoring.listener_factory import ListenerFactory
from interfaces.core import Platform as BasePlatform, TokenInfo as BaseTokenInfo
from platforms import get_platform_implementations
from utils.logger import get_logger

# Constants for post-graduation trading
SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")
PUMP_AMM_PROGRAM_ID = Pubkey.from_string("pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA")
PUMP_SWAP_GLOBAL_CONFIG = Pubkey.from_string("ADyA8hdefvWN2dbGGWFotbzWxrAvLW83WG6QCVXvJKqw")
PUMP_PROTOCOL_FEE_RECIPIENT = Pubkey.from_string("7VtfL8fvgNfhz17qKRMjzQEXgbdpnHHHQRh54R9jP2RJ")
PUMP_PROTOCOL_FEE_RECIPIENT_TOKEN_ACCOUNT = Pubkey.from_string("7GFUN3bWzJMKMRZ34JLsvcqdssDbXnp589SiE33KVwcC")
SYSTEM_TOKEN_PROGRAM = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
SYSTEM_PROGRAM = Pubkey.from_string("11111111111111111111111111111111")
SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
PUMP_SWAP_EVENT_AUTHORITY = Pubkey.from_string("GS4CU59F31iL7aR2Q8zVS8DRrcRnXX1yjQ66TqNVQnaR")

# PumpSwap discriminators
PUMPSWAP_BUY_DISCRIMINATOR = bytes.fromhex("66063d1201daebea")
PUMPSWAP_SELL_DISCRIMINATOR = bytes.fromhex("33e685a4017f83ad")

# Re-export enums and data classes for SDK users
class Platform(Enum):
    """Supported trading platforms."""
    PUMP_FUN = "pump_fun"
    LETS_BONK = "lets_bonk"

class TokenStatus(Enum):
    """Token graduation status."""
    PRE_GRADUATION = "pre_graduation"
    POST_GRADUATION = "post_graduation"

class ListenerType(Enum):
    """Types of token listeners."""
    LOG_SUBSCRIBE = "logs"
    BLOCK_SUBSCRIBE = "block_subscribe"
    GEYSER = "geyser"
    PUMP_PORTAL = "pump_portal"

class TradeType(Enum):
    """Types of trades."""
    BUY = "buy"
    SELL = "sell"

@dataclass
class TokenInfo:
    """Information about a token."""
    name: str
    symbol: str
    description: str
    mint: str
    creator: str
    uri: str
    platform: Platform
    market_cap_sol: Optional[float] = None
    created_timestamp: Optional[int] = None
    bonding_curve: Optional[str] = None
    associated_bonding_curve: Optional[str] = None

    def to_base_token_info(self) -> BaseTokenInfo:
        """Convert to the base TokenInfo used by the underlying system."""
        from solders.pubkey import Pubkey
        
        # Convert platform enum
        base_platform = BasePlatform.PUMP_FUN if self.platform == Platform.PUMP_FUN else BasePlatform.LETS_BONK
        
        return BaseTokenInfo(
            name=self.name,
            symbol=self.symbol,
            uri=self.uri,
            mint=Pubkey.from_string(self.mint),
            platform=base_platform,
            creator=Pubkey.from_string(self.creator) if self.creator else None,
            creation_timestamp=self.created_timestamp,
            bonding_curve=Pubkey.from_string(self.bonding_curve) if self.bonding_curve else None,
            associated_bonding_curve=Pubkey.from_string(self.associated_bonding_curve) if self.associated_bonding_curve else None,
            additional_data={"description": self.description} if self.description else None,
        )

@dataclass
class BondingCurveState:
    """State of a bonding curve."""
    virtual_token_reserves: int
    virtual_sol_reserves: int
    real_token_reserves: int
    real_sol_reserves: int
    token_total_supply: int
    complete: bool

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.token_total_supply <= 0:
            return 0.0
        return ((self.token_total_supply - self.real_token_reserves) / self.token_total_supply) * 100

@dataclass
class TradeResult:
    """Result of a trade execution."""
    success: bool
    signature: Optional[str] = None
    error: Optional[str] = None
    tokens_bought: Optional[int] = None
    tokens_sold: Optional[int] = None
    sol_spent: Optional[float] = None
    sol_received: Optional[float] = None
    price: Optional[float] = None

    @classmethod
    def from_base_trade_result(cls, base_result: BaseTradeResult) -> 'TradeResult':
        """Convert from base TradeResult."""
        return cls(
            success=base_result.success,
            signature=str(base_result.tx_signature) if base_result.tx_signature else None,
            error=base_result.error_message,
            tokens_bought=base_result.amount if base_result.success else None,
            tokens_sold=base_result.amount if base_result.success else None,
            sol_spent=base_result.price if base_result.success else None,
            sol_received=base_result.price if base_result.success else None,
            price=base_result.price,
        )

@dataclass
class Position:
    """Trading position with P&L tracking."""
    token_info: TokenInfo
    tokens_owned: int
    sol_invested: float
    entry_price: float
    entry_time: int
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None
    max_hold_time: Optional[int] = None

    def calculate_pnl(self, current_price: float) -> float:
        """Calculate current profit/loss in SOL."""
        current_value = (self.tokens_owned / 10**6) * current_price
        return current_value - self.sol_invested

    def should_exit(self, current_price: float) -> Tuple[bool, str]:
        """Check if position should be exited."""
        import time
        
        # Take profit
        if self.take_profit and current_price >= self.take_profit:
            return True, "take_profit"
        
        # Stop loss  
        if self.stop_loss and current_price <= self.stop_loss:
            return True, "stop_loss"
        
        # Time-based exit
        if self.max_hold_time and time.time() - self.entry_time > self.max_hold_time:
            return True, "max_hold_time"
        
        return False, ""

class TradingBotSDK:
    """
    Trading Bot SDK - Simplified interface to pump.fun and other DEX trading.
    
    This SDK is a thin wrapper around the existing pump-fun-bot infrastructure,
    providing a clean, simple API while leveraging battle-tested trading logic.
    """
    
    def __init__(
        self,
        private_key: Optional[str] = None,
        rpc_endpoint: Optional[str] = None,
        ws_endpoint: Optional[str] = None,
    ):
        """Initialize the trading bot SDK."""
        self.logger = get_logger(__name__)
        
        # Load environment variables from .env file in pump-fun-bot directory
        env_path = PUMP_BOT_PATH / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        # Load configuration from environment if not provided
        self.private_key = private_key or os.getenv("SOLANA_PRIVATE_KEY")
        self.rpc_endpoint = rpc_endpoint or os.getenv("SOLANA_NODE_RPC_ENDPOINT", "https://mainnet.helius-rpc.com/?api-key=ba80ce11-8c7b-4418-8e85-dc7a3d5d9ca7")
        self.ws_endpoint = ws_endpoint or os.getenv("SOLANA_NODE_WSS_ENDPOINT", "wss://mainnet.helius-rpc.com/?api-key=ba80ce11-8c7b-4418-8e85-dc7a3d5d9ca7")
        
        # Initialize core components
        self.client = SolanaClient(self.rpc_endpoint)
        self.wallet = Wallet(self.private_key) if self.private_key else None
        
        # Initialize priority fee manager
        self.priority_fee_manager = PriorityFeeManager(
            client=self.client,
            enable_dynamic_fee=False,
            enable_fixed_fee=True,
            fixed_fee=200_000,
            extra_fee=0.0,
            hard_cap=500_000,
        )
        
        # State tracking
        self.active_listeners: List[asyncio.Task] = []
        self.positions: Dict[str, Position] = {}
        self.background_listeners: Dict[str, asyncio.Task] = {}
        
    @property
    def wallet_address(self) -> Optional[str]:
        """Get wallet address as string."""
        return str(self.wallet.pubkey) if self.wallet else None
    
    async def wait_for_client_ready(self, timeout: int = 10) -> None:
        """Wait for the client to be ready with a cached blockhash."""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                await self.client.get_cached_blockhash()
                return  # Success, blockhash is cached
            except RuntimeError:
                await asyncio.sleep(0.5)  # Wait 500ms and try again
        raise RuntimeError(f"Client not ready after {timeout} seconds")
    
    async def get_wallet_balance(self) -> float:
        """Get wallet SOL balance."""
        if not self.wallet:
            raise ValueError("No wallet configured")
        
        # Get the underlying AsyncClient and call get_balance
        async_client = await self.client.get_client()
        balance_response = await async_client.get_balance(self.wallet.pubkey)
        balance_lamports = balance_response.value
        return balance_lamports / 1_000_000_000  # Convert to SOL
    
    async def get_token_balance(self, mint: str) -> int:
        """Get token balance for a specific mint."""
        if not self.wallet:
            raise ValueError("No wallet configured")
        
        from solders.pubkey import Pubkey
        from spl.token.instructions import get_associated_token_address
        
        mint_pubkey = Pubkey.from_string(mint)
        ata = get_associated_token_address(self.wallet.pubkey, mint_pubkey)
        
        try:
            balance = await self.client.get_token_account_balance(ata)
            return balance
        except Exception:
            return 0
    
    def derive_bonding_curve_address(self, mint: str, platform: Platform) -> str:
        """Derive bonding curve address for a token."""
        from solders.pubkey import Pubkey
        
        base_platform = BasePlatform.PUMP_FUN if platform == Platform.PUMP_FUN else BasePlatform.LETS_BONK
        implementations = get_platform_implementations(base_platform, self.client)
        
        mint_pubkey = Pubkey.from_string(mint)
        # Use derive_pool_address as that's the bonding curve for pump.fun
        curve_address = implementations.address_provider.derive_pool_address(mint_pubkey)
        
        return str(curve_address)
    
    def derive_associated_bonding_curve_address(self, mint: str, platform: Platform) -> str:
        """Derive associated bonding curve address for a token."""
        from solders.pubkey import Pubkey
        
        base_platform = BasePlatform.PUMP_FUN if platform == Platform.PUMP_FUN else BasePlatform.LETS_BONK
        implementations = get_platform_implementations(base_platform, self.client)
        
        mint_pubkey = Pubkey.from_string(mint)
        # First get the bonding curve address
        bonding_curve = implementations.address_provider.derive_pool_address(mint_pubkey)
        
        # Try to derive the associated bonding curve - not all platforms may have this method
        try:
            assoc_curve_address = implementations.address_provider.derive_associated_bonding_curve(mint_pubkey, bonding_curve)
            return str(assoc_curve_address)
        except AttributeError:
            # Fallback for platforms that don't have this method
            from spl.token.instructions import get_associated_token_address
            return str(get_associated_token_address(bonding_curve, mint_pubkey))
    
    async def get_bonding_curve_state(self, mint: str, platform: Platform) -> BondingCurveState:
        """Get bonding curve state for a token."""
        from solders.pubkey import Pubkey
        
        base_platform = BasePlatform.PUMP_FUN if platform == Platform.PUMP_FUN else BasePlatform.LETS_BONK
        implementations = get_platform_implementations(base_platform, self.client)
        
        mint_pubkey = Pubkey.from_string(mint)
        curve_address = implementations.address_provider.derive_pool_address(mint_pubkey)
        
        # Get curve state using existing curve manager
        curve_data = await implementations.curve_manager.get_pool_state(curve_address)
        
        return BondingCurveState(
            virtual_token_reserves=curve_data["virtual_token_reserves"],
            virtual_sol_reserves=curve_data["virtual_sol_reserves"],
            real_token_reserves=curve_data["real_token_reserves"],
            real_sol_reserves=curve_data["real_sol_reserves"],
            token_total_supply=curve_data["token_total_supply"],
            complete=curve_data["complete"],
        )
    
    def calculate_token_price(self, curve_state: BondingCurveState) -> float:
        """Calculate token price from bonding curve state."""
        if curve_state.virtual_token_reserves <= 0 or curve_state.virtual_sol_reserves <= 0:
            raise ValueError("Invalid reserve state")
        
        LAMPORTS_PER_SOL = 1_000_000_000
        TOKEN_DECIMALS = 6
        
        return (curve_state.virtual_sol_reserves / LAMPORTS_PER_SOL) / (
            curve_state.virtual_token_reserves / 10**TOKEN_DECIMALS
        )
    
    def calculate_buy_amount(self, curve_state: BondingCurveState, sol_amount: float) -> int:
        """Calculate tokens received for SOL amount."""
        if curve_state.virtual_token_reserves <= 0 or curve_state.virtual_sol_reserves <= 0:
            return 0
        
        sol_lamports = int(sol_amount * 1_000_000_000)
        
        # Simple AMM formula: tokens_out = (token_reserves * sol_in) / (sol_reserves + sol_in)
        tokens_out = (curve_state.virtual_token_reserves * sol_lamports) // (curve_state.virtual_sol_reserves + sol_lamports)
        
        return max(0, tokens_out)
    
    def calculate_sell_amount(self, curve_state: BondingCurveState, token_amount: int) -> int:
        """Calculate SOL received for token amount."""
        if curve_state.virtual_token_reserves <= 0 or curve_state.virtual_sol_reserves <= 0:
            return 0
        
        # Simple AMM formula: sol_out = (sol_reserves * tokens_in) / (token_reserves + tokens_in)
        sol_out = (curve_state.virtual_sol_reserves * token_amount) // (curve_state.virtual_token_reserves + token_amount)
        
        return max(0, sol_out)
    
    async def get_token_price(self, mint: str, platform: Platform) -> float:
        """Get current token price."""
        curve_state = await self.get_bonding_curve_state(mint, platform)
        return self.calculate_token_price(curve_state)
    
    async def get_token_status(self, mint: str) -> TokenStatus:
        """Determine if a token is pre or post graduation."""
        from solders.pubkey import Pubkey
        mint_pubkey = Pubkey.from_string(mint)
        
        try:
            # Try to get bonding curve state first
            base_platform = BasePlatform.PUMP_FUN
            implementations = get_platform_implementations(base_platform, self.client)
            curve_address = implementations.address_provider.derive_pool_address(mint_pubkey)
            
            # Get curve state using existing curve manager
            curve_data = await implementations.curve_manager.get_pool_state(curve_address)
            
            if curve_data.get("complete", False):
                return TokenStatus.POST_GRADUATION
            else:
                return TokenStatus.PRE_GRADUATION
                
        except Exception:
            # If bonding curve doesn't exist, try to find AMM market
            try:
                async_client = await self.client.get_client()
                await self._get_pumpswap_market_address(async_client, mint_pubkey)
                return TokenStatus.POST_GRADUATION
            except Exception:
                # Default to pre-graduation if we can't determine
                return TokenStatus.PRE_GRADUATION

    async def _get_pumpswap_market_address(self, client: AsyncClient, base_mint: Pubkey) -> Pubkey:
        """Find the PumpSwap AMM market address for a given token mint."""
        try:
            all_response = await client.get_program_accounts(PUMP_AMM_PROGRAM_ID, encoding="base64")
            
            if not all_response.value:
                raise ValueError("No AMM accounts returned from RPC")

            for account in all_response.value:
                try:
                    data = account.account.data
                    if len(data) > 75:
                        potential_mint_bytes = data[43:43+32]
                        potential_mint = Pubkey.from_bytes(potential_mint_bytes)
                        
                        if potential_mint == base_mint:
                            return account.pubkey
                except Exception:
                    continue
                    
        except Exception as e:
            raise ValueError(f"Failed to search PumpSwap markets: {e}")
            
        raise ValueError("No PumpSwap market found for this token")

    async def _get_pumpswap_market_data(self, client: AsyncClient, market_address: Pubkey) -> Dict[str, Any]:
        """Fetch and parse PumpSwap market data."""
        response = await client.get_account_info(market_address, encoding="base64")
        if not response.value or not response.value.data:
            raise ValueError("Invalid market data")
            
        data = response.value.data
        parsed_data = {}

        offset = 8
        fields = [
            ("pool_bump", "u8"),
            ("index", "u16"),
            ("creator", "pubkey"),
            ("base_mint", "pubkey"),
            ("quote_mint", "pubkey"),
            ("lp_mint", "pubkey"),
            ("pool_base_token_account", "pubkey"),
            ("pool_quote_token_account", "pubkey"),
            ("lp_supply", "u64"),
            ("coin_creator", "pubkey")
        ]

        for field_name, field_type in fields:
            if field_type == "pubkey":
                value = data[offset:offset + 32]
                parsed_data[field_name] = base58.b58encode(value).decode("utf-8")
                offset += 32
            elif field_type in {"u64", "i64"}:
                fmt = "<Q" if field_type == "u64" else "<q"
                value = struct.unpack(fmt, data[offset:offset + 8])[0]
                parsed_data[field_name] = value
                offset += 8
            elif field_type == "u16":
                value = struct.unpack("<H", data[offset:offset + 2])[0]
                parsed_data[field_name] = value
                offset += 2
            elif field_type == "u8":
                value = data[offset]
                parsed_data[field_name] = value
                offset += 1

        return parsed_data

    def _find_coin_creator_vault(self, coin_creator: Pubkey) -> Pubkey:
        """Derive the Program Derived Address (PDA) for a coin creator's vault."""
        derived_address, _ = Pubkey.find_program_address(
            [b"creator_vault", bytes(coin_creator)],
            PUMP_AMM_PROGRAM_ID,
        )
        return derived_address

    def _find_global_volume_accumulator(self) -> Pubkey:
        """Derive the Program Derived Address (PDA) for the global volume accumulator."""
        derived_address, _ = Pubkey.find_program_address(
            [b"global_volume_accumulator"],
            PUMP_AMM_PROGRAM_ID,
        )
        return derived_address

    def _find_user_volume_accumulator(self, user: Pubkey) -> Pubkey:
        """Derive the Program Derived Address (PDA) for a user's volume accumulator."""
        derived_address, _ = Pubkey.find_program_address(
            [b"user_volume_accumulator", bytes(user)],
            PUMP_AMM_PROGRAM_ID,
        )
        return derived_address

    async def _calculate_pumpswap_price(
        self, 
        client: AsyncClient, 
        pool_base_token_account: Pubkey, 
        pool_quote_token_account: Pubkey
    ) -> float:
        """Calculate token price in PumpSwap AMM pool based on reserves."""
        base_balance_resp = await client.get_token_account_balance(pool_base_token_account)
        quote_balance_resp = await client.get_token_account_balance(pool_quote_token_account)
            
        base_amount = float(base_balance_resp.value.ui_amount or 0)
        quote_amount = float(quote_balance_resp.value.ui_amount or 0)

        if base_amount == 0:
            return 0.0
            
        return quote_amount / base_amount

    async def buy_token(
        self,
        mint: str,
        sol_amount: float,
        platform: Platform,
        slippage: float = 0.05
    ) -> TradeResult:
        """Universal buy function - automatically detects pre/post graduation."""
        if not self.wallet:
            raise ValueError("No wallet configured for trading")
        
        try:
            # Determine token status
            status = await self.get_token_status(mint)
            
            if status == TokenStatus.PRE_GRADUATION:
                self.logger.info(f"Buying pre-graduation token via bonding curve")
                # Ensure client is ready
                await self.wait_for_client_ready()
                return await self._buy_token_pumpfun(mint, sol_amount, platform, slippage)
            else:
                self.logger.info(f"Buying post-graduation token via PumpSwap AMM")
                return await self._buy_token_pumpswap(mint, sol_amount, slippage)
                
        except Exception as e:
            self.logger.error(f"Buy failed: {e}")
            return TradeResult(
                success=False,
                error=str(e)
            )
    
    async def _buy_token_pumpfun(
        self,
        mint: str,
        sol_amount: float,
        platform: Platform,
        slippage: float
    ) -> TradeResult:
        """Buy token using pump.fun bonding curve."""
        # Derive addresses needed for trading
        bonding_curve_addr = self.derive_bonding_curve_address(mint, platform)
        assoc_bonding_curve_addr = self.derive_associated_bonding_curve_address(mint, platform)
        
        # Create TokenInfo with proper addresses
        token_info = TokenInfo(
            name="Unknown",
            symbol="UNK",
            description="Token for trading",
            mint=mint,
            creator="11111111111111111111111111111111",
            uri="",
            platform=platform,
            bonding_curve=bonding_curve_addr,
            associated_bonding_curve=assoc_bonding_curve_addr
        )
        
        # Convert to base token info
        base_token_info = token_info.to_base_token_info()
        
        # Create buyer
        buyer = PlatformAwareBuyer(
            client=self.client,
            wallet=self.wallet,
            priority_fee_manager=self.priority_fee_manager,
            amount=sol_amount,
            slippage=slippage,
            max_retries=3,
        )
        
        # Execute buy
        result = await buyer.execute(base_token_info)
        return TradeResult.from_base_trade_result(result)

    async def _buy_token_pumpswap(
        self,
        mint: str,
        sol_amount: float,
        slippage: float = 0.25
    ) -> TradeResult:
        """Buy tokens using PumpSwap AMM (post-graduation only)."""
        try:
            from solders.pubkey import Pubkey
            mint_pubkey = Pubkey.from_string(mint)
            
            async_client = await self.client.get_client()
            
            # Get market data
            market_address = await self._get_pumpswap_market_address(async_client, mint_pubkey)
            market_data = await self._get_pumpswap_market_data(async_client, market_address)
            
            # Calculate required addresses
            coin_creator_vault_authority = self._find_coin_creator_vault(
                Pubkey.from_string(market_data["coin_creator"])
            )
            coin_creator_vault_ata = get_associated_token_address(coin_creator_vault_authority, SOL_MINT)
            
            # Use the working buy function
            tx_hash = await self._buy_pump_swap_token(
                async_client,
                market_address,
                self.wallet,
                mint_pubkey,
                Pubkey.from_string(market_data["pool_base_token_account"]),
                Pubkey.from_string(market_data["pool_quote_token_account"]),
                coin_creator_vault_authority,
                coin_creator_vault_ata,
                sol_amount,
                slippage
            )
            
            return TradeResult(success=True, signature=tx_hash)
            
        except Exception as e:
            return TradeResult(success=False, error=str(e))

    async def _buy_pump_swap_token(
        self,
        client: AsyncClient,
        market_address: Pubkey,
        payer: Keypair,
        base_mint: Pubkey,
        pool_base_token_account: Pubkey,
        pool_quote_token_account: Pubkey,
        coin_creator_vault_authority: Pubkey,
        coin_creator_vault_ata: Pubkey,
        sol_amount_to_spend: float,
        slippage: float = 0.25
    ) -> str:
        """Buy tokens on the PUMP AMM with slippage protection."""
        # Calculate token price
        token_price_sol = await self._calculate_pumpswap_price(client, pool_base_token_account, pool_quote_token_account)

        # Calculate amounts
        base_amount_out = int((sol_amount_to_spend / token_price_sol) * 10**6)
        slippage_factor = 1 + slippage
        max_sol_input = int((sol_amount_to_spend * slippage_factor) * 1_000_000_000)

        # Get user accounts
        user_base_token_account = get_associated_token_address(payer.pubkey(), base_mint)
        user_quote_token_account = get_associated_token_address(payer.pubkey(), SOL_MINT)
        
        # Calculate required PDAs
        global_volume_accumulator = self._find_global_volume_accumulator()
        user_volume_accumulator = self._find_user_volume_accumulator(payer.pubkey())

        # Build transaction accounts
        accounts = [
            AccountMeta(pubkey=market_address, is_signer=False, is_writable=False),
            AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=PUMP_SWAP_GLOBAL_CONFIG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=base_mint, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SOL_MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=user_base_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=user_quote_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=pool_base_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=pool_quote_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PUMP_PROTOCOL_FEE_RECIPIENT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_PROTOCOL_FEE_RECIPIENT_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_SWAP_EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_AMM_PROGRAM_ID, is_signer=False, is_writable=False),
            AccountMeta(pubkey=coin_creator_vault_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=coin_creator_vault_authority, is_signer=False, is_writable=False),
            AccountMeta(pubkey=global_volume_accumulator, is_signer=False, is_writable=True),
            AccountMeta(pubkey=user_volume_accumulator, is_signer=False, is_writable=True),
        ]
        
        # Build instruction data
        data = PUMPSWAP_BUY_DISCRIMINATOR + struct.pack("<Q", base_amount_out) + struct.pack("<Q", max_sol_input)

        # Build instructions
        compute_limit_ix = set_compute_unit_limit(200_000)
        compute_price_ix = set_compute_unit_price(10_000)
        
        # Create WSOL ATA
        create_wsol_ata_ix = create_idempotent_associated_token_account(
            payer.pubkey(),
            payer.pubkey(),
            SOL_MINT,
            SYSTEM_TOKEN_PROGRAM
        )
        
        # Calculate wrap amount with buffer for fees
        pump_protocol_fees = sol_amount_to_spend * 0.1
        wrap_amount = int((sol_amount_to_spend + pump_protocol_fees) * 1_000_000_000)
        
        # Transfer and wrap SOL
        transfer_sol_ix = transfer(
            TransferParams(
                from_pubkey=payer.pubkey(),
                to_pubkey=user_quote_token_account,
                lamports=wrap_amount
            )
        )
        
        sync_native_ix = sync_native(
            SyncNativeParams(SYSTEM_TOKEN_PROGRAM, user_quote_token_account)
        )
        
        # Create token ATA
        idempotent_ata_ix = create_idempotent_associated_token_account(
            payer.pubkey(),
            payer.pubkey(),
            base_mint,
            SYSTEM_TOKEN_PROGRAM
        )
        
        # Main buy instruction
        buy_ix = Instruction(PUMP_AMM_PROGRAM_ID, data, accounts)
        
        # Build transaction
        blockhash_resp = await client.get_latest_blockhash()
        recent_blockhash = blockhash_resp.value.blockhash

        msg = Message.new_with_blockhash(
            [compute_limit_ix, compute_price_ix, create_wsol_ata_ix, transfer_sol_ix, sync_native_ix, idempotent_ata_ix, buy_ix],
            payer.pubkey(),
            recent_blockhash
        )

        tx_buy = VersionedTransaction(
            message=msg,
            keypairs=[payer]
        )
        
        # Simulate transaction
        simulation = await client.simulate_transaction(tx_buy)
        if simulation.value.err:
            raise Exception(f"Transaction simulation failed: {simulation.value.err}")
        
        # Send transaction
        tx_sig = await client.send_transaction(
            tx_buy,
            opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed),
        )
        
        tx_hash = tx_sig.value
        await client.confirm_transaction(tx_hash, commitment="confirmed")
        return str(tx_hash)
    
    async def sell_token(
        self,
        mint: str,
        platform: Platform,
        slippage: float = 0.05
    ) -> TradeResult:
        """Universal sell function - automatically detects pre/post graduation."""
        if not self.wallet:
            raise ValueError("No wallet configured for trading")
        
        try:
            # Determine token status
            status = await self.get_token_status(mint)
            
            if status == TokenStatus.PRE_GRADUATION:
                self.logger.info(f"Selling pre-graduation token via bonding curve")
                # Ensure client is ready
                await self.wait_for_client_ready()
                return await self._sell_token_pumpfun(mint, platform, slippage)
            else:
                self.logger.info(f"Selling post-graduation token via PumpSwap AMM")
                return await self._sell_token_pumpswap(mint, slippage)
                
        except Exception as e:
            self.logger.error(f"Sell failed: {e}")
            return TradeResult(
                success=False,
                error=str(e)
            )

    async def _sell_token_pumpfun(
        self,
        mint: str,
        platform: Platform,
        slippage: float
    ) -> TradeResult:
        """Sell token using pump.fun bonding curve."""
        # Derive addresses needed for trading
        bonding_curve_addr = self.derive_bonding_curve_address(mint, platform)
        assoc_bonding_curve_addr = self.derive_associated_bonding_curve_address(mint, platform)
        
        # Create TokenInfo with proper addresses
        token_info = TokenInfo(
            name="Unknown",
            symbol="UNK",
            description="Token for trading",
            mint=mint,
            creator="11111111111111111111111111111111",
            uri="",
            platform=platform,
            bonding_curve=bonding_curve_addr,
            associated_bonding_curve=assoc_bonding_curve_addr
        )
        
        # Convert to base token info
        base_token_info = token_info.to_base_token_info()
        
        # Create seller
        seller = PlatformAwareSeller(
            client=self.client,
            wallet=self.wallet,
            priority_fee_manager=self.priority_fee_manager,
            slippage=slippage,
            max_retries=3,
        )
        
        # Execute sell
        result = await seller.execute(base_token_info)
        return TradeResult.from_base_trade_result(result)

    async def _sell_token_pumpswap(
        self,
        mint: str,
        slippage: float = 0.25
    ) -> TradeResult:
        """Sell tokens using PumpSwap AMM (post-graduation only)."""
        try:
            from solders.pubkey import Pubkey
            mint_pubkey = Pubkey.from_string(mint)
            
            async_client = await self.client.get_client()
            
            # Get market data
            market_address = await self._get_pumpswap_market_address(async_client, mint_pubkey)
            market_data = await self._get_pumpswap_market_data(async_client, market_address)
            
            # Calculate required addresses
            coin_creator_vault_authority = self._find_coin_creator_vault(
                Pubkey.from_string(market_data["coin_creator"])
            )
            coin_creator_vault_ata = get_associated_token_address(coin_creator_vault_authority, SOL_MINT)
            
            # Use the working sell function
            tx_hash = await self._sell_pump_swap_token(
                async_client,
                market_address,
                self.wallet,
                mint_pubkey,
                Pubkey.from_string(market_data["pool_base_token_account"]),
                Pubkey.from_string(market_data["pool_quote_token_account"]),
                coin_creator_vault_authority,
                coin_creator_vault_ata,
                slippage
            )
            
            return TradeResult(success=True, signature=tx_hash)
            
        except Exception as e:
            return TradeResult(success=False, error=str(e))

    async def _sell_pump_swap_token(
        self,
        client: AsyncClient,
        market_address: Pubkey,
        payer: Keypair,
        base_mint: Pubkey,
        pool_base_token_account: Pubkey,
        pool_quote_token_account: Pubkey,
        coin_creator_vault_authority: Pubkey,
        coin_creator_vault_ata: Pubkey,
        slippage: float = 0.25
    ) -> str:
        """Sell tokens on the PUMP AMM with slippage protection."""
        # Get user accounts
        user_base_token_account = get_associated_token_address(payer.pubkey(), base_mint)
        user_quote_token_account = get_associated_token_address(payer.pubkey(), SOL_MINT)
        
        # Get token balance
        try:
            token_balance_resp = await client.get_token_account_balance(user_base_token_account)
            token_balance = int(token_balance_resp.value.amount)
        except Exception as e:
            raise Exception("Could not get token balance - do you have any tokens to sell?")
        
        token_balance_decimal = token_balance / 10**6
        
        if token_balance == 0:
            raise Exception("No tokens to sell")
        
        # Calculate token price
        token_price_sol = await self._calculate_pumpswap_price(client, pool_base_token_account, pool_quote_token_account)
        
        # Calculate minimum SOL output with slippage protection
        expected_sol_output = float(token_balance_decimal) * float(token_price_sol)
        slippage_factor = 1 - slippage
        min_sol_output = int((expected_sol_output * slippage_factor) * 1_000_000_000)

        # Build transaction accounts
        accounts = [
            AccountMeta(pubkey=market_address, is_signer=False, is_writable=False),
            AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=PUMP_SWAP_GLOBAL_CONFIG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=base_mint, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SOL_MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=user_base_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=user_quote_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=pool_base_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=pool_quote_token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PUMP_PROTOCOL_FEE_RECIPIENT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_PROTOCOL_FEE_RECIPIENT_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_SWAP_EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_AMM_PROGRAM_ID, is_signer=False, is_writable=False),
            AccountMeta(pubkey=coin_creator_vault_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=coin_creator_vault_authority, is_signer=False, is_writable=False),
        ]
        
        # Build instruction data
        data = PUMPSWAP_SELL_DISCRIMINATOR + struct.pack("<Q", token_balance) + struct.pack("<Q", min_sol_output)

        # Build instructions
        compute_limit_ix = set_compute_unit_limit(100_000)
        compute_price_ix = set_compute_unit_price(10_000)
        
        # Create WSOL ATA (in case it doesn't exist)
        create_wsol_ata_ix = create_idempotent_associated_token_account(
            payer.pubkey(),
            payer.pubkey(),
            SOL_MINT,
            SYSTEM_TOKEN_PROGRAM
        )
        
        # Main sell instruction
        sell_ix = Instruction(PUMP_AMM_PROGRAM_ID, data, accounts)
        
        # Build transaction
        blockhash_resp = await client.get_latest_blockhash()
        recent_blockhash = blockhash_resp.value.blockhash

        msg = Message.new_with_blockhash(
            [compute_limit_ix, compute_price_ix, create_wsol_ata_ix, sell_ix],
            payer.pubkey(),
            recent_blockhash
        )

        tx_sell = VersionedTransaction(
            message=msg,
            keypairs=[payer]
        )
        
        # Simulate transaction
        simulation = await client.simulate_transaction(tx_sell)
        if simulation.value.err:
            raise Exception(f"Transaction simulation failed: {simulation.value.err}")
        
        # Send transaction
        tx_sig = await client.send_transaction(
            tx_sell,
            opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed),
        )
        
        tx_hash = tx_sig.value
        await client.confirm_transaction(tx_hash, commitment="confirmed")
        return str(tx_hash)
    
    async def listen_new_tokens(
        self,
        callback: Callable[[TokenInfo], None],
        listener_type: ListenerType = ListenerType.LOG_SUBSCRIBE,
        platforms: List[Platform] = None
    ) -> None:
        """Listen for new token creations."""
        if platforms is None:
            platforms = [Platform.PUMP_FUN]
        
        # Convert to base platforms
        base_platforms = []
        for platform in platforms:
            if platform == Platform.PUMP_FUN:
                base_platforms.append(BasePlatform.PUMP_FUN)
            elif platform == Platform.LETS_BONK:
                base_platforms.append(BasePlatform.LETS_BONK)
        
        # Create listener
        listener = ListenerFactory.create_listener(
            listener_type=listener_type.value,
            wss_endpoint=self.ws_endpoint,
            platforms=base_platforms,
        )
        
        # Wrapper callback to convert TokenInfo
        def wrapper_callback(base_token_info: BaseTokenInfo):
            try:
                # Convert to SDK TokenInfo
                sdk_platform = Platform.PUMP_FUN if base_token_info.platform == BasePlatform.PUMP_FUN else Platform.LETS_BONK
                
                sdk_token_info = TokenInfo(
                    name=base_token_info.name,
                    symbol=base_token_info.symbol,
                    description=getattr(base_token_info, 'description', ''),
                    mint=str(base_token_info.mint),
                    creator=str(base_token_info.creator) if base_token_info.creator else '',
                    uri=base_token_info.uri,
                    platform=sdk_platform,
                    created_timestamp=base_token_info.creation_timestamp,
                    bonding_curve=str(base_token_info.bonding_curve) if base_token_info.bonding_curve else None,
                    associated_bonding_curve=str(base_token_info.associated_bonding_curve) if base_token_info.associated_bonding_curve else None,
                )
                
                callback(sdk_token_info)
            except Exception as e:
                self.logger.error(f"Error in token callback: {e}")
        
        # Start listening
        task = asyncio.create_task(
            listener.listen_for_tokens(wrapper_callback, None, None)
        )
        self.active_listeners.append(task)
    
    
    def stop_all_listeners(self) -> None:
        """Stop all active listeners."""
        for task in self.active_listeners:
            task.cancel()
        self.active_listeners.clear()
    
    async def close(self) -> None:
        """Clean up and close SDK resources."""
        self.stop_all_listeners()
        await self.client.close()


# Initialize MCP server
mcp = FastMCP("PumpFun Trading Bot")

# Global SDK instance (will be initialized on first use)
_sdk_instance: Optional[TradingBotSDK] = None

async def get_sdk() -> TradingBotSDK:
    """Get or create SDK instance."""
    global _sdk_instance
    if _sdk_instance is None:
        _sdk_instance = TradingBotSDK()
        await _sdk_instance.wait_for_client_ready()
    return _sdk_instance

# MCP Tools
@mcp.tool()
async def get_wallet_balance() -> str:
    """Get the wallet's SOL balance in SOL units."""
    sdk = await get_sdk()
    balance = await sdk.get_wallet_balance()
    return f"{balance:.6f} SOL"

@mcp.tool()
async def get_wallet_address() -> str:
    """Get the wallet's public address."""
    sdk = await get_sdk()
    return str(sdk.wallet_address)

@mcp.tool()
async def get_token_balance(mint: str) -> str:
    """Get the balance of a specific SPL token.
    
    Args:
        mint: The token mint address (e.g., 'So11111111111111111111111111111111111111112' for WSOL)
    """
    sdk = await get_sdk()
    balance = await sdk.get_token_balance(mint)
    return f"{balance} raw units ({balance / 1_000_000:.6f} tokens)"

@mcp.tool()
async def get_token_price(mint: str) -> str:
    """Get the current price of a pump.fun token in SOL.
    
    Args:
        mint: The token mint address
    """
    sdk = await get_sdk()
    try:
        price = await sdk.get_token_price(mint, Platform.PUMP_FUN)
        return f"{price:.10f} SOL per token"
    except Exception as e:
        return f"Error getting price: {str(e)}"

@mcp.tool()
async def get_bonding_curve_state(mint: str) -> str:
    """Get the bonding curve state for a pump.fun token.
    
    Args:
        mint: The token mint address
    """
    sdk = await get_sdk()
    try:
        state = await sdk.get_bonding_curve_state(mint, Platform.PUMP_FUN)
        return f"Complete: {state.complete}, Progress: {state.completion_percentage:.2f}%, Virtual SOL: {state.virtual_sol_reserves / 1_000_000_000:.6f}, Virtual Tokens: {state.virtual_token_reserves / 1_000_000:.2f}"
    except Exception as e:
        return f"Error getting curve state: {str(e)}"

@mcp.tool()
async def buy_token(mint: str, sol_amount: float, slippage: float = 0.05) -> str:
    """Universal buy function - automatically detects pre/post graduation and uses appropriate method.
    
    Args:
        mint: The token mint address
        sol_amount: Amount of SOL to spend (e.g., 0.001 for 0.001 SOL)
        slippage: Maximum slippage tolerance (default 0.05 = 5%)
    """
    sdk = await get_sdk()
    try:
        result = await sdk.buy_token(mint, sol_amount, Platform.PUMP_FUN, slippage)
        if result.success:
            return f"✅ Buy successful! TX: {result.signature}, Tokens bought: {result.tokens_bought}, SOL spent: {result.sol_spent}"
        else:
            return f"❌ Buy failed: {result.error}"
    except Exception as e:
        return f"Error executing buy: {str(e)}"

@mcp.tool()
async def sell_token(mint: str, slippage: float = 0.05) -> str:
    """Universal sell function - automatically detects pre/post graduation and uses appropriate method.
    
    Args:
        mint: The token mint address
        slippage: Maximum slippage tolerance (default 0.05 = 5%)
    """
    sdk = await get_sdk()
    try:
        result = await sdk.sell_token(mint, Platform.PUMP_FUN, slippage)
        if result.success:
            return f"✅ Sell successful! TX: {result.signature}, Tokens sold: {result.tokens_sold}, SOL received: {result.sol_received}"
        else:
            return f"❌ Sell failed: {result.error}"
    except Exception as e:
        return f"Error executing sell: {str(e)}"

@mcp.tool()
async def get_token_status(mint: str) -> str:
    """Check if a token is pre-graduation (bonding curve) or post-graduation (PumpSwap AMM).
    
    Args:
        mint: The token mint address
    """
    sdk = await get_sdk()
    try:
        status = await sdk.get_token_status(mint)
        if status == TokenStatus.PRE_GRADUATION:
            return f"Token {mint} is PRE-GRADUATION (bonding curve)"
        else:
            return f"Token {mint} is POST-GRADUATION (PumpSwap AMM)"
    except Exception as e:
        return f"Error checking token status: {str(e)}"

@mcp.tool()
async def calculate_buy_amount(mint: str, sol_amount: float) -> str:
    """Calculate how many tokens you would get for a given SOL amount.
    
    Args:
        mint: The token mint address
        sol_amount: Amount of SOL to simulate spending
    """
    sdk = await get_sdk()
    try:
        curve_state = await sdk.get_bonding_curve_state(mint, Platform.PUMP_FUN)
        token_amount = sdk.calculate_buy_amount(curve_state, sol_amount)
        return f"For {sol_amount} SOL you would get approximately {token_amount / 1_000_000:.6f} tokens"
    except Exception as e:
        return f"Error calculating buy amount: {str(e)}"

@mcp.tool()
async def derive_bonding_curve_address(mint: str) -> str:
    """Derive the bonding curve address for a token.
    
    Args:
        mint: The token mint address
    """
    sdk = await get_sdk()
    try:
        curve_addr = sdk.derive_bonding_curve_address(mint, Platform.PUMP_FUN)
        assoc_curve_addr = sdk.derive_associated_bonding_curve_address(mint, Platform.PUMP_FUN)
        return f"Bonding curve: {curve_addr}, Associated curve: {assoc_curve_addr}"
    except Exception as e:
        return f"Error deriving addresses: {str(e)}"

@mcp.tool()
async def start_token_listener_with_logging(duration_seconds: int = 21600, log_file: str = "new_tokens.json") -> str:
    """Start a background token listener that logs new pump.fun tokens to JSON file.
    
    Args:
        duration_seconds: How long to listen in seconds (default 21600 = 6 hours)
        log_file: JSON file to save tokens to (default "new_tokens.json")
    """
    import json
    import time
    from pathlib import Path
    
    sdk = await get_sdk()
    
    # Check if listener already running
    listener_key = f"listener_{log_file}"
    if listener_key in sdk.background_listeners:
        task = sdk.background_listeners[listener_key]
        if not task.done():
            return f"Token listener already running for {log_file}. Use stop_token_listener() to stop it."
    
    # Load existing tokens if file exists
    log_path = Path(log_file)
    existing_tokens = []
    if log_path.exists():
        try:
            with open(log_path, 'r') as f:
                existing_tokens = json.load(f)
        except:
            existing_tokens = []
    
    tokens_found_count = 0
    
    def token_callback(token_info):
        nonlocal tokens_found_count
        token_data = {
            "mint": token_info.mint,
            "symbol": token_info.symbol,
            "name": token_info.name,
            "creator": token_info.creator,
            "bonding_curve": token_info.bonding_curve,
            "associated_bonding_curve": token_info.associated_bonding_curve,
            "timestamp": int(time.time()),
            "platform": token_info.platform.value
        }
        existing_tokens.append(token_data)
        tokens_found_count += 1
        
        # Save immediately when new token is found
        try:
            with open(log_path, 'w') as f:
                json.dump(existing_tokens, f, indent=2)
        except:
            pass  # Ignore file write errors
    
    async def background_listener():
        """Background listener task"""
        try:
            await sdk.listen_new_tokens(token_callback, platforms=[Platform.PUMP_FUN])
            await asyncio.sleep(duration_seconds)
        except Exception as e:
            print(f"Background listener error: {e}")
        finally:
            sdk.stop_all_listeners()
            # Remove from background listeners
            if hasattr(sdk, 'background_listeners') and listener_key in sdk.background_listeners:
                del sdk.background_listeners[listener_key]
    
    # Start background task
    task = asyncio.create_task(background_listener())
    sdk.background_listeners[listener_key] = task
    
    return f"✅ Started background token listener for {duration_seconds/3600:.1f} hours. Logging to {log_file}. Use stop_token_listener() to stop."

@mcp.tool()
async def stop_token_listener(log_file: str = "new_tokens.json") -> str:
    """Stop the background token listener.
    
    Args:
        log_file: Log file name to identify which listener to stop
    """
    sdk = await get_sdk()
    listener_key = f"listener_{log_file}"
    
    if listener_key not in sdk.background_listeners:
        return f"No active listener found for {log_file}"
    
    task = sdk.background_listeners[listener_key]
    if task.done():
        del sdk.background_listeners[listener_key]
        return f"Listener for {log_file} had already stopped"
    
    # Cancel the background task
    task.cancel()
    sdk.stop_all_listeners()
    
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    del sdk.background_listeners[listener_key]
    return f"✅ Stopped token listener for {log_file}"

@mcp.tool()
async def check_listener_status(log_file: str = "new_tokens.json") -> str:
    """Check if a token listener is currently running.
    
    Args:
        log_file: Log file name to check listener status for
    """
    sdk = await get_sdk()
    listener_key = f"listener_{log_file}"
    
    if listener_key not in sdk.background_listeners:
        return f"❌ No listener running for {log_file}"
    
    task = sdk.background_listeners[listener_key]
    if task.done():
        del sdk.background_listeners[listener_key]
        return f"❌ Listener for {log_file} has stopped"
    
    return f"✅ Listener active for {log_file}, running in background"

@mcp.tool()
async def read_logged_tokens(log_file: str = "new_tokens.json", hours_ago: int = 24) -> str:
    """Read logged tokens from JSON file and filter by time.
    
    Args:
        log_file: JSON file to read tokens from (default "new_tokens.json")
        hours_ago: Only return tokens created within this many hours (default 24)
    """
    import json
    import time
    from pathlib import Path
    
    log_path = Path(log_file)
    if not log_path.exists():
        return f"Log file {log_file} does not exist"
    
    try:
        with open(log_path, 'r') as f:
            all_tokens = json.load(f)
        
        # Filter tokens by time
        cutoff_time = int(time.time()) - (hours_ago * 3600)
        recent_tokens = [t for t in all_tokens if t.get('timestamp', 0) > cutoff_time]
        
        if not recent_tokens:
            return f"No tokens found in the last {hours_ago} hours"
        
        token_summary = []
        for token in recent_tokens:
            hours_old = (int(time.time()) - token.get('timestamp', 0)) / 3600
            token_summary.append(f"{token['symbol']} ({token['mint'][:8]}...) - {hours_old:.1f}h ago")
        
        return f"Found {len(recent_tokens)} tokens in the last {hours_ago} hours:\n" + "\n".join(token_summary)
    except Exception as e:
        return f"Error reading log file: {str(e)}"

@mcp.tool()
async def analyze_logged_tokens_bonding_curves(log_file: str = "new_tokens.json", hours_ago: int = 1, max_tokens: int = 10) -> str:
    """Analyze bonding curves of recently logged tokens to find the best trading opportunities.
    
    Args:
        log_file: JSON file to read tokens from (default "new_tokens.json")
        hours_ago: Only analyze tokens created within this many hours (default 1)
        max_tokens: Maximum number of tokens to analyze (default 10)
    """
    import json
    import time
    from pathlib import Path
    
    log_path = Path(log_file)
    if not log_path.exists():
        return f"Log file {log_file} does not exist"
    
    try:
        with open(log_path, 'r') as f:
            all_tokens = json.load(f)
        
        # Filter tokens by time
        cutoff_time = int(time.time()) - (hours_ago * 3600)
        recent_tokens = [t for t in all_tokens if t.get('timestamp', 0) > cutoff_time]
        
        if not recent_tokens:
            return f"No tokens found in the last {hours_ago} hours"
        
        # Limit the number of tokens to analyze
        tokens_to_analyze = recent_tokens[:max_tokens]
        
        sdk = await get_sdk()
        token_analysis = []
        
        # Analyze each token's bonding curve
        for token in tokens_to_analyze:
            try:
                state = await sdk.get_bonding_curve_state(token['mint'], Platform.PUMP_FUN)
                sol_reserves = state.virtual_sol_reserves / 1_000_000_000  # Convert to SOL
                token_price = sdk.calculate_token_price(state)
                
                analysis = {
                    "mint": token['mint'],
                    "symbol": token['symbol'],
                    "sol_reserves": sol_reserves,
                    "completion_percent": state.completion_percentage,
                    "token_price": token_price,
                    "is_complete": state.complete,
                    "age_hours": (int(time.time()) - token.get('timestamp', 0)) / 3600
                }
                token_analysis.append(analysis)
            except Exception as e:
                continue  # Skip tokens that error
        
        if not token_analysis:
            return "Could not analyze any tokens - they may have errors or be migrated"
        
        # Sort by SOL reserves (highest first)
        token_analysis.sort(key=lambda x: x['sol_reserves'], reverse=True)
        
        # Format results
        results = []
        for i, analysis in enumerate(token_analysis[:5], 1):  # Top 5 results
            results.append(
                f"{i}. {analysis['symbol']} ({analysis['mint'][:8]}...)\n"
                f"   SOL Reserves: {analysis['sol_reserves']:.4f} SOL\n"
                f"   Completion: {analysis['completion_percent']:.1f}%\n"
                f"   Price: {analysis['token_price']:.10f} SOL/token\n"
                f"   Age: {analysis['age_hours']:.1f}h\n"
                f"   Complete: {analysis['is_complete']}"
            )
        
        best_token = token_analysis[0]
        recommendation = f"\n🎯 RECOMMENDED: {best_token['symbol']} ({best_token['mint']}) with {best_token['sol_reserves']:.4f} SOL reserves"
        
        return f"Analyzed {len(token_analysis)} tokens:\n\n" + "\n\n".join(results) + recommendation
        
    except Exception as e:
        return f"Error analyzing tokens: {str(e)}"

@mcp.tool()
async def execute_trading_strategy(hours_ago: int = 1, buy_amount: float = 0.001, max_tokens_to_analyze: int = 10) -> str:
    """Execute the full trading strategy: analyze recent tokens and buy the best one.
    
    Args:
        hours_ago: Only consider tokens created within this many hours (default 1)
        buy_amount: Amount of SOL to spend on the selected token (default 0.001)
        max_tokens_to_analyze: Maximum number of tokens to analyze (default 10)
    """
    import json
    import time
    from pathlib import Path
    
    log_file = "new_tokens.json"
    log_path = Path(log_file)
    
    if not log_path.exists():
        return f"No token log file found. Run start_token_listener_with_logging first."
    
    try:
        # Read and filter tokens
        with open(log_path, 'r') as f:
            all_tokens = json.load(f)
        
        cutoff_time = int(time.time()) - (hours_ago * 3600)
        recent_tokens = [t for t in all_tokens if t.get('timestamp', 0) > cutoff_time]
        
        if not recent_tokens:
            return f"No tokens found in the last {hours_ago} hours to analyze"
        
        tokens_to_analyze = recent_tokens[:max_tokens_to_analyze]
        sdk = await get_sdk()
        
        # Analyze bonding curves
        valid_tokens = []
        for token in tokens_to_analyze:
            try:
                state = await sdk.get_bonding_curve_state(token['mint'], Platform.PUMP_FUN)
                if state.complete:
                    continue  # Skip completed tokens
                
                sol_reserves = state.virtual_sol_reserves / 1_000_000_000
                token_price = sdk.calculate_token_price(state)
                
                valid_tokens.append({
                    "mint": token['mint'],
                    "symbol": token['symbol'],
                    "sol_reserves": sol_reserves,
                    "completion_percent": state.completion_percentage,
                    "token_price": token_price,
                    "age_hours": (int(time.time()) - token.get('timestamp', 0)) / 3600
                })
            except:
                continue
        
        if not valid_tokens:
            return "No valid tokens found for trading (all may be completed or have errors)"
        
        # Select best token (highest SOL reserves)
        best_token = max(valid_tokens, key=lambda x: x['sol_reserves'])
        
        # Execute buy
        result = await sdk.buy_token(best_token['mint'], buy_amount, Platform.PUMP_FUN, 0.05)
        
        strategy_summary = (
            f"📊 STRATEGY EXECUTION SUMMARY:\n"
            f"Analyzed {len(tokens_to_analyze)} recent tokens\n"
            f"Found {len(valid_tokens)} valid trading candidates\n"
            f"Selected: {best_token['symbol']} ({best_token['mint'][:8]}...)\n"
            f"SOL Reserves: {best_token['sol_reserves']:.4f} SOL\n"
            f"Completion: {best_token['completion_percent']:.1f}%\n"
            f"Age: {best_token['age_hours']:.1f} hours\n"
            f"Buy Amount: {buy_amount} SOL\n\n"
        )
        
        if result.success:
            return (strategy_summary + 
                   f"✅ TRADE SUCCESSFUL!\n"
                   f"TX: {result.signature}\n"
                   f"Tokens bought: {result.tokens_bought}\n"
                   f"SOL spent: {result.sol_spent}")
        else:
            return (strategy_summary + 
                   f"❌ TRADE FAILED: {result.error}")
            
    except Exception as e:
        return f"Error executing trading strategy: {str(e)}"


if __name__ == "__main__":
    print("Starting PumpFun Trading Bot MCP server...")
    mcp.run()