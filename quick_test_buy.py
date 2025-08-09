#!/usr/bin/env python3
"""
Quick test script for buying tokens with fixed implementation
"""

import asyncio
from trading_bot_sdk import TradingBotSDK, Platform

async def test_buy():
    """Quick test of token purchase"""
    # Test tokens
    PRE_GRAD_TOKEN = "3qA4yBZBPGvEyk36jUrS65UGJ2ACu1fTtFxMv3kfpump"   # Pre-graduation
    POST_GRAD_TOKEN = "6qHtAvksH2cSaUjz6euVSikPU8RnDqLpFtuWH6Ropump"  # Post-graduation
    
    sdk = TradingBotSDK()
    
    try:
        await sdk.wait_for_client_ready()
        
        balance = await sdk.get_wallet_balance()
        print(f"Wallet balance: {balance:.6f} SOL")
        print(f"Wallet address: {sdk.wallet_address}")
        
        # Test pre-graduation token first (smaller amount)
        print(f"\n🧪 Testing PRE-GRADUATION token: {PRE_GRAD_TOKEN}")
        
        try:
            result = await sdk.buy_token(
                mint=PRE_GRAD_TOKEN,
                sol_amount=0.001,  # 0.001 SOL
                platform=Platform.PUMP_FUN,
                slippage=0.1  # 10% slippage
            )
            
            if result.success:
                print(f"✅ Pre-graduation buy successful!")
                print(f"   TX: {result.signature}")
                print(f"   Tokens: {result.tokens_bought}")
                print(f"   SOL spent: {result.sol_spent}")
            else:
                print(f"❌ Pre-graduation buy failed: {result.error}")
                
        except Exception as e:
            print(f"❌ Pre-graduation error: {e}")
        
        # Test post-graduation token with smaller timeout
        print(f"\n🧪 Testing POST-GRADUATION token: {POST_GRAD_TOKEN}")
        
        try:
            result = await sdk.buy_token(
                mint=POST_GRAD_TOKEN,
                sol_amount=0.001,  # 0.001 SOL
                platform=Platform.PUMP_FUN,
                slippage=0.1  # 10% slippage
            )
            
            if result.success:
                print(f"✅ Post-graduation buy successful!")
                print(f"   TX: {result.signature}")
                print(f"   Tokens: {result.tokens_bought}")
                print(f"   SOL spent: {result.sol_spent}")
            else:
                print(f"❌ Post-graduation buy failed: {result.error}")
                
        except Exception as e:
            print(f"❌ Post-graduation error: {e}")
            
    finally:
        await sdk.close()

if __name__ == "__main__":
    asyncio.run(test_buy())