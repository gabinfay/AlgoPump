#!/usr/bin/env python3
"""
Fixed pump.fun buy implementation based on manual_buy.py
This handles pre-graduation tokens correctly with all required accounts
"""

import asyncio
import struct
import os
from typing import Optional, Tuple
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.message import Message
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from spl.token.instructions import (
    create_idempotent_associated_token_account,
    get_associated_token_address,
)
import base58

# Constants from manual_buy.py
PUMP_PROGRAM = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
PUMP_GLOBAL = Pubkey.from_string("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf")
PUMP_EVENT_AUTHORITY = Pubkey.from_string("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1")
PUMP_FEE = Pubkey.from_string("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM")
SYSTEM_PROGRAM = Pubkey.from_string("11111111111111111111111111111111")
SYSTEM_TOKEN_PROGRAM = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
SOL = Pubkey.from_string("So11111111111111111111111111111111111111112")
LAMPORTS_PER_SOL = 1_000_000_000
TOKEN_DECIMALS = 6

# Discriminators
BUY_DISCRIMINATOR = struct.pack("<Q", 16927863322537952870)
EXPECTED_CURVE_DISCRIMINATOR = struct.pack("<Q", 6966180631402821399)


def derive_pump_addresses(mint: Pubkey) -> Tuple[Pubkey, Pubkey]:
    """Derive bonding curve and associated bonding curve addresses."""
    # Bonding curve PDA
    bonding_curve, _ = Pubkey.find_program_address(
        [b"bonding-curve", bytes(mint)],
        PUMP_PROGRAM
    )
    
    # Associated bonding curve is the token account for the bonding curve
    associated_bonding_curve = get_associated_token_address(bonding_curve, mint)
    
    return bonding_curve, associated_bonding_curve


def find_creator_vault(creator: Pubkey) -> Pubkey:
    """Find the creator vault PDA."""
    derived_address, _ = Pubkey.find_program_address(
        [b"creator-vault", bytes(creator)],
        PUMP_PROGRAM,
    )
    return derived_address


def find_global_volume_accumulator() -> Pubkey:
    """Find the global volume accumulator PDA."""
    derived_address, _ = Pubkey.find_program_address(
        [b"global_volume_accumulator"],
        PUMP_PROGRAM,
    )
    return derived_address


def find_user_volume_accumulator(user: Pubkey) -> Pubkey:
    """Find the user volume accumulator PDA."""
    derived_address, _ = Pubkey.find_program_address(
        [b"user_volume_accumulator", bytes(user)],
        PUMP_PROGRAM,
    )
    return derived_address


class BondingCurveState:
    """Parse bonding curve account data."""
    def __init__(self, data: bytes):
        if data[:8] != EXPECTED_CURVE_DISCRIMINATOR:
            raise ValueError("Invalid curve state discriminator")
        
        # Parse the data after discriminator
        offset = 8
        self.virtual_token_reserves = struct.unpack("<Q", data[offset:offset+8])[0]
        offset += 8
        self.virtual_sol_reserves = struct.unpack("<Q", data[offset:offset+8])[0]
        offset += 8
        self.real_token_reserves = struct.unpack("<Q", data[offset:offset+8])[0]
        offset += 8
        self.real_sol_reserves = struct.unpack("<Q", data[offset:offset+8])[0]
        offset += 8
        self.token_total_supply = struct.unpack("<Q", data[offset:offset+8])[0]
        offset += 8
        self.complete = bool(data[offset])
        offset += 1
        self.creator = Pubkey.from_bytes(data[offset:offset+32])


async def get_pump_curve_state(client: AsyncClient, curve_address: Pubkey) -> BondingCurveState:
    """Fetch and parse bonding curve state."""
    response = await client.get_account_info(curve_address, encoding="base64")
    if not response.value or not response.value.data:
        raise ValueError("Invalid curve state: No data")
    
    return BondingCurveState(response.value.data)


def calculate_pump_curve_price(curve_state: BondingCurveState) -> float:
    """Calculate token price from bonding curve state."""
    if curve_state.virtual_token_reserves <= 0 or curve_state.virtual_sol_reserves <= 0:
        raise ValueError("Invalid reserve state")
    
    return (curve_state.virtual_sol_reserves / LAMPORTS_PER_SOL) / (
        curve_state.virtual_token_reserves / 10**TOKEN_DECIMALS
    )


async def buy_pump_fun_token(
    client: AsyncClient,
    payer: Keypair,
    mint: Pubkey,
    sol_amount: float,
    slippage: float = 0.25,
    max_retries: int = 3
) -> str:
    """Buy pre-graduation pump.fun token."""
    print(f"Buying token {mint} with {sol_amount} SOL")
    
    # Derive addresses
    bonding_curve, associated_bonding_curve = derive_pump_addresses(mint)
    print(f"Bonding curve: {bonding_curve}")
    print(f"Associated bonding curve: {associated_bonding_curve}")
    
    # Get curve state to find creator
    curve_state = await get_pump_curve_state(client, bonding_curve)
    creator_vault = find_creator_vault(curve_state.creator)
    print(f"Creator: {curve_state.creator}")
    print(f"Creator vault: {creator_vault}")
    
    # Calculate token price and amount
    token_price_sol = calculate_pump_curve_price(curve_state)
    print(f"Token price: {token_price_sol:.10f} SOL")
    
    # Calculate expected token amount
    token_amount = sol_amount / token_price_sol
    print(f"Expected tokens: {token_amount:.2f}")
    
    # Get user's associated token account
    associated_token_account = get_associated_token_address(payer.pubkey(), mint)
    
    # Convert SOL to lamports
    amount_lamports = int(sol_amount * LAMPORTS_PER_SOL)
    max_amount_lamports = int(amount_lamports * (1 + slippage))
    
    # Build accounts list (order matters!)
    accounts = [
        AccountMeta(pubkey=PUMP_GLOBAL, is_signer=False, is_writable=False),
        AccountMeta(pubkey=PUMP_FEE, is_signer=False, is_writable=True),
        AccountMeta(pubkey=mint, is_signer=False, is_writable=False),
        AccountMeta(pubkey=bonding_curve, is_signer=False, is_writable=True),
        AccountMeta(pubkey=associated_bonding_curve, is_signer=False, is_writable=True),
        AccountMeta(pubkey=associated_token_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
        AccountMeta(pubkey=creator_vault, is_signer=False, is_writable=True),
        AccountMeta(pubkey=PUMP_EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(pubkey=PUMP_PROGRAM, is_signer=False, is_writable=False),
        AccountMeta(pubkey=find_global_volume_accumulator(), is_signer=False, is_writable=True),
        AccountMeta(pubkey=find_user_volume_accumulator(payer.pubkey()), is_signer=False, is_writable=True),
    ]
    
    # Build instruction data
    data = (
        BUY_DISCRIMINATOR +
        struct.pack("<Q", int(token_amount * 10**6)) +  # Token amount with decimals
        struct.pack("<Q", max_amount_lamports)  # Max SOL to spend
    )
    
    # Create buy instruction
    buy_ix = Instruction(PUMP_PROGRAM, data, accounts)
    
    # Create associated token account if needed
    idempotent_ata_ix = create_idempotent_associated_token_account(
        payer.pubkey(), payer.pubkey(), mint
    )
    
    # Build transaction
    recent_blockhash = await client.get_latest_blockhash()
    
    msg = Message.new_with_blockhash(
        [
            set_compute_unit_limit(300_000),
            set_compute_unit_price(10_000),
            idempotent_ata_ix,
            buy_ix
        ],
        payer.pubkey(),
        recent_blockhash.value.blockhash
    )
    
    # Create and sign transaction
    tx = VersionedTransaction(message=msg, keypairs=[payer])
    
    # Send with retries
    for attempt in range(max_retries):
        try:
            print(f"Sending transaction (attempt {attempt + 1}/{max_retries})...")
            
            # Send transaction
            result = await client.send_transaction(
                tx,
                opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed)
            )
            
            tx_hash = result.value
            print(f"Transaction sent: {tx_hash}")
            
            # Confirm transaction
            await client.confirm_transaction(tx_hash, commitment="confirmed")
            print("Transaction confirmed!")
            
            return str(tx_hash)
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                raise Exception(f"Failed after {max_retries} attempts: {str(e)}")


async def test_buy():
    """Test buying both tokens."""
    # Load private key
    private_key = os.getenv("SOLANA_PRIVATE_KEY")
    if not private_key:
        raise ValueError("SOLANA_PRIVATE_KEY not set")
    
    payer = Keypair.from_bytes(base58.b58decode(private_key))
    print(f"Wallet: {payer.pubkey()}")
    
    # RPC endpoint
    rpc_endpoint = os.getenv("SOLANA_NODE_RPC_ENDPOINT", "https://mainnet.helius-rpc.com/?api-key=ba80ce11-8c7b-4418-8e85-dc7a3d5d9ca7")
    
    # Test tokens
    tokens = [
        ("Pre-graduation", "3qA4yBZBPGvEyk36jUrS65UGJ2ACu1fTtFxMv3kfpump"),
        # ("Post-graduation", "6qHtAvksH2cSaUjz6euVSikPU8RnDqLpFtuWH6Ropump"),
    ]
    
    async with AsyncClient(rpc_endpoint) as client:
        # Get balance
        balance_resp = await client.get_balance(payer.pubkey())
        balance = balance_resp.value / LAMPORTS_PER_SOL
        print(f"Balance: {balance:.6f} SOL\n")
        
        for name, mint_str in tokens:
            print(f"\n{'='*60}")
            print(f"Testing {name} token: {mint_str}")
            print(f"{'='*60}")
            
            try:
                mint = Pubkey.from_string(mint_str)
                tx_hash = await buy_pump_fun_token(
                    client,
                    payer,
                    mint,
                    sol_amount=0.001,  # 0.001 SOL
                    slippage=0.1  # 10% slippage
                )
                print(f"✅ Success! Transaction: https://solscan.io/tx/{tx_hash}")
                
            except Exception as e:
                print(f"❌ Failed: {e}")
            
            # Wait between tests
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(test_buy())