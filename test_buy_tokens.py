#!/usr/bin/env python3
"""
Test script to buy both pre-graduation and post-graduation tokens
"""

import asyncio
import logging
from trading_bot_sdk import TradingBotSDK, Platform, TokenStatus

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Token addresses
POST_GRAD_TOKEN = "6qHtAvksH2cSaUjz6euVSikPU8RnDqLpFtuWH6Ropump"  # Post-graduation
PRE_GRAD_TOKEN = "3qA4yBZBPGvEyk36jUrS65UGJ2ACu1fTtFxMv3kfpump"   # Pre-graduation

# Buy amount in SOL
BUY_AMOUNT = 0.001  # 0.001 SOL (minimum reasonable amount)

async def test_buy_tokens():
    """Test buying both tokens"""
    print("Starting test_buy_tokens...")
    
    # Initialize SDK
    print("Creating SDK instance...")
    sdk = TradingBotSDK()
    
    try:
        # Wait for client to be ready
        print("Initializing SDK...")
        await sdk.wait_for_client_ready()
        print("SDK initialized successfully")
        
        # Get wallet balance
        print("Getting wallet balance...")
        balance = await sdk.get_wallet_balance()
        print(f"\nWallet balance: {balance:.6f} SOL")
        print(f"Wallet address: {sdk.wallet_address}")
        
        # Test 1: Buy post-graduation token
        print(f"\n{'='*60}")
        print(f"TEST 1: Buying POST-GRADUATION token")
        print(f"Token: {POST_GRAD_TOKEN}")
        print(f"Amount: {BUY_AMOUNT} SOL")
        print(f"{'='*60}")
        
        try:
            # Check token status
            print("Checking token status...")
            status = await sdk.get_token_status(POST_GRAD_TOKEN)
            print(f"Token status: {status.value}")
            
            if status == TokenStatus.POST_GRADUATION:
                print("Confirmed: Token is post-graduation, will use PumpSwap AMM")
            else:
                print("WARNING: Token status is not post-graduation as expected!")
            
            # Execute buy
            print(f"\nExecuting buy order for {BUY_AMOUNT} SOL...")
            print("Calling sdk.buy_token()...")
            
            result = await sdk.buy_token(
                mint=POST_GRAD_TOKEN,
                sol_amount=BUY_AMOUNT,
                platform=Platform.PUMP_FUN,
                slippage=0.05
            )
            
            print("Buy token call completed, checking result...")
            
            if result.success:
                print(f"✅ Buy successful!")
                print(f"   Transaction: {result.signature}")
                print(f"   Tokens bought: {result.tokens_bought}")
                print(f"   SOL spent: {result.sol_spent}")
            else:
                print(f"❌ Buy failed: {result.error}")
                
        except Exception as e:
            print(f"❌ Error buying post-graduation token: {e}")
            import traceback
            traceback.print_exc()
        
        # Add a small delay between trades
        print("\nWaiting 2 seconds before next trade...")
        await asyncio.sleep(2)
        
        # Test 2: Buy pre-graduation token
        print(f"\n{'='*60}")
        print(f"TEST 2: Buying PRE-GRADUATION token")
        print(f"Token: {PRE_GRAD_TOKEN}")
        print(f"Amount: {BUY_AMOUNT} SOL")
        print(f"{'='*60}")
        
        try:
            # Check token status
            print("Checking token status...")
            status = await sdk.get_token_status(PRE_GRAD_TOKEN)
            print(f"Token status: {status.value}")
            
            if status == TokenStatus.PRE_GRADUATION:
                print("Confirmed: Token is pre-graduation, will use bonding curve")
            else:
                print("WARNING: Token status is not pre-graduation as expected!")
            
            # Execute buy
            print(f"\nExecuting buy order for {BUY_AMOUNT} SOL...")
            print("Calling sdk.buy_token()...")
            
            result = await sdk.buy_token(
                mint=PRE_GRAD_TOKEN,
                sol_amount=BUY_AMOUNT,
                platform=Platform.PUMP_FUN,
                slippage=0.05
            )
            
            print("Buy token call completed, checking result...")
            
            if result.success:
                print(f"✅ Buy successful!")
                print(f"   Transaction: {result.signature}")
                print(f"   Tokens bought: {result.tokens_bought}")
                print(f"   SOL spent: {result.sol_spent}")
            else:
                print(f"❌ Buy failed: {result.error}")
                
        except Exception as e:
            print(f"❌ Error buying pre-graduation token: {e}")
            import traceback
            traceback.print_exc()
        
        # Final balance check
        print("\nGetting final wallet balance...")
        final_balance = await sdk.get_wallet_balance()
        print(f"\n{'='*60}")
        print(f"Final wallet balance: {final_balance:.6f} SOL")
        print(f"Total SOL spent: {balance - final_balance:.6f} SOL")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        print("\nCleaning up SDK resources...")
        await sdk.close()
        print("Test completed!")

if __name__ == "__main__":
    print("Starting asyncio event loop...")
    asyncio.run(test_buy_tokens())