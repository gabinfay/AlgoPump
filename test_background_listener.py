#!/usr/bin/env python3
"""
Test script for the background listener functionality
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

async def test_background_listener():
    """Test the background listener functionality"""
    
    print("🚀 Testing Background Token Listener")
    print("=" * 50)
    
    # Initialize SDK
    sdk = TradingBotSDK()
    await sdk.wait_for_client_ready()
    
    print(f"✅ SDK initialized")
    print(f"💰 Wallet: {sdk.wallet_address}")
    
    # Test background listener management
    import json
    import time
    from pathlib import Path
    
    log_file = "background_test.json"
    listener_key = f"listener_{log_file}"
    
    # 1. Start background listener
    print("\n🎧 Starting background listener for 60 seconds...")
    
    # Check if listener already running
    if listener_key in sdk.background_listeners:
        task = sdk.background_listeners[listener_key]
        if not task.done():
            print("⚠️ Listener already running, stopping it first...")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del sdk.background_listeners[listener_key]
    
    # Load existing tokens if file exists
    log_path = Path(log_file)
    existing_tokens = []
    if log_path.exists():
        try:
            with open(log_path, 'r') as f:
                existing_tokens = json.load(f)
        except:
            existing_tokens = []
    
    print(f"📝 Starting with {len(existing_tokens)} existing tokens")
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
        
        print(f"🔍 Found token #{tokens_found_count}: {token_data['symbol']} ({token_data['mint']})")
        
        # Save immediately when new token is found
        try:
            with open(log_path, 'w') as f:
                json.dump(existing_tokens, f, indent=2)
        except:
            pass  # Ignore file write errors
    
    async def background_listener():
        """Background listener task"""
        try:
            print("👂 Background listener started...")
            await sdk.listen_new_tokens(token_callback, platforms=[Platform.PUMP_FUN])
            await asyncio.sleep(60)  # 1 minute for testing
            print("⏰ Background listener duration completed")
        except Exception as e:
            print(f"❌ Background listener error: {e}")
        finally:
            sdk.stop_all_listeners()
            if listener_key in sdk.background_listeners:
                del sdk.background_listeners[listener_key]
            print("🛑 Background listener stopped")
    
    # Start background task
    task = asyncio.create_task(background_listener())
    sdk.background_listeners[listener_key] = task
    
    print(f"✅ Background listener started! Task ID: {id(task)}")
    
    # 2. Test that we can do other operations while listener runs
    print("\n🔧 Testing other operations while listener runs in background...")
    
    # Test wallet operations
    try:
        balance = await sdk.get_wallet_balance()
        print(f"✅ Can get wallet balance: {balance:.6f} SOL")
    except Exception as e:
        print(f"❌ Failed to get wallet balance: {e}")
    
    # Test bonding curve analysis of known token
    try:
        test_mint = "47sfyWY62hjMhzrQ8VshpY8yv3Hsf6pq3Qqf4Bhdpump"
        state = await sdk.get_bonding_curve_state(test_mint, Platform.PUMP_FUN)
        sol_reserves = state.virtual_sol_reserves / 1_000_000_000
        print(f"✅ Can analyze bonding curves: {sol_reserves:.4f} SOL reserves")
    except Exception as e:
        print(f"❌ Failed to analyze bonding curve: {e}")
    
    # 3. Check listener status periodically
    print("\n📊 Monitoring listener status...")
    for i in range(3):  # Check 3 times over 30 seconds
        await asyncio.sleep(10)
        
        # Check if task is still running
        if listener_key in sdk.background_listeners:
            task_status = sdk.background_listeners[listener_key]
            if task_status.done():
                print(f"⚠️ Background task completed at check #{i+1}")
                del sdk.background_listeners[listener_key]
                break
            else:
                print(f"✅ Background listener still active at check #{i+1} - found {tokens_found_count} tokens so far")
        else:
            print(f"❌ Background listener not found at check #{i+1}")
            break
    
    # 4. Stop the listener manually if still running
    print("\n🛑 Stopping background listener...")
    if listener_key in sdk.background_listeners:
        task = sdk.background_listeners[listener_key]
        if not task.done():
            task.cancel()
            sdk.stop_all_listeners()
            
            try:
                await task
            except asyncio.CancelledError:
                print("✅ Background task cancelled successfully")
            
            del sdk.background_listeners[listener_key]
        else:
            print("✅ Background task had already completed")
            del sdk.background_listeners[listener_key]
    else:
        print("ℹ️ No active background listener to stop")
    
    # 5. Check final results
    print(f"\n📈 Final Results:")
    print(f"🔍 Total tokens found during test: {tokens_found_count}")
    
    if log_path.exists():
        try:
            with open(log_path, 'r') as f:
                final_tokens = json.load(f)
            print(f"💾 Total tokens in log file: {len(final_tokens)}")
            
            # Show latest tokens
            if final_tokens:
                print("🆕 Latest tokens:")
                for token in final_tokens[-3:]:  # Show last 3
                    hours_old = (int(time.time()) - token.get('timestamp', 0)) / 3600
                    print(f"   - {token['symbol']} ({token['mint'][:8]}...) - {hours_old:.1f}h ago")
        except:
            print("❌ Could not read final log file")
    
    print("\n🏁 Background listener test completed!")
    
    # Cleanup
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(test_background_listener())