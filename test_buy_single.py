#!/usr/bin/env python3
"""
Simple test script to buy a single token
"""

import asyncio
import sys
import logging
from trading_bot_sdk import TradingBotSDK, Platform, TokenStatus

# Enable detailed logging
logging.basicConfig(
    level=logging.INFO,  # Use INFO instead of DEBUG to reduce noise
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_buy_single_token(token_address: str, amount: float = 0.001):
    """Test buying a single token"""
    print(f"\nTesting purchase of token: {token_address}")
    print(f"Amount: {amount} SOL")
    
    # Initialize SDK
    sdk = TradingBotSDK()
    
    try:
        # Wait for client to be ready
        print("Initializing SDK...")
        await sdk.wait_for_client_ready()
        
        # Get wallet info
        balance = await sdk.get_wallet_balance()
        print(f"Wallet balance: {balance:.6f} SOL")
        print(f"Wallet address: {sdk.wallet_address}")
        
        # Check if we have enough balance
        if balance < amount + 0.01:  # Include some buffer for fees
            print(f"❌ Insufficient balance. Need at least {amount + 0.01} SOL")
            return
        
        # Check token status
        print("\nChecking token status...")
        try:
            status = await sdk.get_token_status(token_address)
            print(f"Token status: {status.value}")
        except Exception as e:
            print(f"Warning: Could not determine token status: {e}")
            print("Attempting to buy anyway...")
        
        # Execute buy
        print(f"\nExecuting buy order for {amount} SOL...")
        result = await sdk.buy_token(
            mint=token_address,
            sol_amount=amount,
            platform=Platform.PUMP_FUN,
            slippage=0.10  # 10% slippage for testing
        )
        
        if result.success:
            print(f"\n✅ Buy successful!")
            print(f"Transaction: {result.signature}")
            if result.tokens_bought:
                print(f"Tokens bought: {result.tokens_bought}")
            if result.sol_spent:
                print(f"SOL spent: {result.sol_spent}")
            
            # Check token balance
            try:
                token_balance = await sdk.get_token_balance(token_address)
                print(f"New token balance: {token_balance}")
            except:
                pass
        else:
            print(f"\n❌ Buy failed: {result.error}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        await sdk.close()
        print("\nTest completed!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_buy_single.py <token_address> [amount_sol]")
        print("\nExample tokens:")
        print("  Post-grad: 6qHtAvksH2cSaUjz6euVSikPU8RnDqLpFtuWH6Ropump")
        print("  Pre-grad:  3qA4yBZBPGvEyk36jUrS65UGJ2ACu1fTtFxMv3kfpump")
        sys.exit(1)
    
    token_address = sys.argv[1]
    amount = float(sys.argv[2]) if len(sys.argv) > 2 else 0.001
    
    asyncio.run(test_buy_single_token(token_address, amount))

if __name__ == "__main__":
    main()