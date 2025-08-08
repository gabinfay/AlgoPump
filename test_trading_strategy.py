#!/usr/bin/env python3
"""
Test script for the trading strategy functions
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the pump-fun-bot source to path  
PUMP_BOT_PATH = Path(__file__).parent / "pump-fun-bot"
PUMP_BOT_SRC_PATH = PUMP_BOT_PATH / "src"
if str(PUMP_BOT_PATH) not in sys.path:
    sys.path.insert(0, str(PUMP_BOT_PATH))
if str(PUMP_BOT_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(PUMP_BOT_SRC_PATH))

# Import the SDK
from trading_bot_sdk import TradingBotSDK, Platform

async def test_trading_strategy():
    """Test the full trading strategy workflow"""
    
    print("🚀 Testing Trading Strategy Functions")
    print("=" * 50)
    
    # Initialize SDK
    sdk = TradingBotSDK()
    await sdk.wait_for_client_ready()
    
    print(f"✅ SDK initialized")
    print(f"💰 Wallet: {sdk.wallet_address}")
    
    # Test 1: Check wallet balance
    print("\n📊 Testing wallet balance...")
    try:
        balance = await sdk.get_wallet_balance()
        print(f"✅ Wallet balance: {balance:.6f} SOL")
    except Exception as e:
        print(f"❌ Wallet balance failed: {e}")
        return
    
    # Test 2: Start token listener (short duration for testing)
    print("\n🎧 Testing token listener with JSON logging...")
    try:
        import json
        import time
        from pathlib import Path
        
        log_file = "test_new_tokens.json"
        log_path = Path(log_file)
        
        # Load existing tokens if file exists
        existing_tokens = []
        if log_path.exists():
            try:
                with open(log_path, 'r') as f:
                    existing_tokens = json.load(f)
            except:
                existing_tokens = []
        
        print(f"📝 Existing tokens in log: {len(existing_tokens)}")
        
        found_tokens = []
        def token_callback(token_info):
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
            print(f"🔍 Found new token: {token_data['symbol']} ({token_data['mint']})")
            found_tokens.append(token_data)
            existing_tokens.append(token_data)
        
        # Listen for 30 seconds
        print("👂 Listening for new tokens for 30 seconds...")
        await sdk.listen_new_tokens(token_callback, platforms=[Platform.PUMP_FUN])
        await asyncio.sleep(30)
        sdk.stop_all_listeners()
        
        # Save to file
        with open(log_path, 'w') as f:
            json.dump(existing_tokens, f, indent=2)
        
        print(f"✅ Found {len(found_tokens)} new tokens, saved to {log_file}")
        
    except Exception as e:
        print(f"❌ Token listener failed: {e}")
    
    # Test 3: Read logged tokens
    print("\n📖 Testing read logged tokens...")
    try:
        import json
        import time
        
        if not Path("test_new_tokens.json").exists():
            print("⚠️ No token log file found, creating sample data...")
            # Create sample data for testing
            sample_tokens = [
                {
                    "mint": "47sfyWY62hjMhzrQ8VshpY8yv3Hsf6pq3Qqf4Bhdpump",
                    "symbol": "TEST1",
                    "name": "Test Token 1",
                    "creator": "11111111111111111111111111111111",
                    "bonding_curve": None,
                    "associated_bonding_curve": None,
                    "timestamp": int(time.time()) - 1800,  # 30 minutes ago
                    "platform": "pump_fun"
                }
            ]
            with open("test_new_tokens.json", 'w') as f:
                json.dump(sample_tokens, f, indent=2)
        
        with open("test_new_tokens.json", 'r') as f:
            all_tokens = json.load(f)
        
        cutoff_time = int(time.time()) - (24 * 3600)  # 24 hours ago
        recent_tokens = [t for t in all_tokens if t.get('timestamp', 0) > cutoff_time]
        
        print(f"✅ Found {len(recent_tokens)} tokens in the last 24 hours")
        for token in recent_tokens[:3]:  # Show first 3
            hours_old = (int(time.time()) - token.get('timestamp', 0)) / 3600
            print(f"   - {token['symbol']} ({token['mint'][:8]}...) - {hours_old:.1f}h ago")
            
    except Exception as e:
        print(f"❌ Read logged tokens failed: {e}")
    
    # Test 4: Analyze bonding curves
    print("\n🔍 Testing bonding curve analysis...")
    try:
        import json
        import time
        
        with open("test_new_tokens.json", 'r') as f:
            all_tokens = json.load(f)
        
        # Take first few tokens for analysis
        tokens_to_analyze = all_tokens[:3] if len(all_tokens) >= 3 else all_tokens
        
        print(f"🧪 Analyzing {len(tokens_to_analyze)} tokens...")
        
        token_analysis = []
        for token in tokens_to_analyze:
            try:
                print(f"   🔬 Analyzing {token['symbol']} ({token['mint'][:8]}...)")
                state = await sdk.get_bonding_curve_state(token['mint'], Platform.PUMP_FUN)
                sol_reserves = state.virtual_sol_reserves / 1_000_000_000
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
                
                print(f"      💰 SOL Reserves: {sol_reserves:.4f}")
                print(f"      📈 Completion: {state.completion_percentage:.1f}%")
                print(f"      💲 Price: {token_price:.10f} SOL/token")
                print(f"      ✅ Complete: {state.complete}")
                
            except Exception as e:
                print(f"      ❌ Failed to analyze {token['symbol']}: {e}")
                continue
        
        if token_analysis:
            # Sort by SOL reserves
            token_analysis.sort(key=lambda x: x['sol_reserves'], reverse=True)
            best_token = token_analysis[0]
            
            print(f"\n🎯 BEST TOKEN: {best_token['symbol']} ({best_token['mint'][:8]}...)")
            print(f"   💰 SOL Reserves: {best_token['sol_reserves']:.4f}")
            print(f"   📊 Completion: {best_token['completion_percent']:.1f}%")
            print(f"   ⏰ Age: {best_token['age_hours']:.1f}h")
        else:
            print("⚠️ No tokens could be analyzed")
            
    except Exception as e:
        print(f"❌ Bonding curve analysis failed: {e}")
    
    # Test 5: Test buying (with very small amount)
    print("\n💰 Testing token purchase...")
    try:
        # Use the best token from analysis if available
        if 'best_token' in locals() and not best_token['is_complete']:
            mint_to_buy = best_token['mint']
            symbol_to_buy = best_token['symbol']
            
            print(f"🎯 Attempting to buy {symbol_to_buy} ({mint_to_buy[:8]}...)")
            print(f"💸 Amount: 0.00001 SOL")
            
            # Very small test purchase
            result = await sdk.buy_token(mint_to_buy, 0.00001, Platform.PUMP_FUN, 0.05)
            
            if result.success:
                print(f"✅ Purchase successful!")
                print(f"   📋 TX: {result.signature}")
                print(f"   🪙 Tokens bought: {result.tokens_bought}")
                print(f"   💰 SOL spent: {result.sol_spent}")
            else:
                print(f"❌ Purchase failed: {result.error}")
        else:
            print("⚠️ No valid tokens available for purchase test")
            
    except Exception as e:
        print(f"❌ Token purchase test failed: {e}")
    
    print("\n🏁 Trading strategy test completed!")
    
    # Cleanup
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(test_trading_strategy())