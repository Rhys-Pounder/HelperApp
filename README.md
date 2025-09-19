# AWS Log Checker Helper

A comprehensive tool for tracking AWS log checks and generating professional evidence packs. Available as both a desktop GUI application and a cross-platform web application.

## 🌟 Features

- **Log Check Tracking**: Record and manage AWS log check sessions with timestamps, outcomes, and detailed notes
- **Evidence Pack Generation**: Create professional documentation with dynamic sections for findings, actions, and follow-ups
- **AWS Query Library**: Pre-built CloudWatch Insights queries and AWS CLI commands for common troubleshooting scenarios
- **History Management**: View, search, export, and manage historical check records
- **Reminder System**: Automated reminders for scheduled log checks (desktop version)
- **Modern UI**: Dark theme with responsive design and intuitive navigation
- **Cross-Platform**: Available as desktop app (macOS/Windows/Linux) and web app (Docker)

## 🚀 Quick Start

### Option 1: Web Application (Recommended - No Dependencies)

The web version runs in Docker and works on any platform without GUI dependencies:

```bash
# Clone the repository
git clone <repository-url>
cd HelperApp

# Start the web application
./run-docker.sh

# Open your browser to:
# http://localhost:8080
```

### Option 2: Desktop GUI Application

For native desktop experience with system integration:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the desktop application
python main.py
```

## 📋 Requirements

### Web Version (Docker)
- Docker installed and running
- Web browser (Chrome, Firefox, Safari, etc.)

### Desktop Version
- Python 3.8+
- tkinter (usually included with Python)
- customtkinter
- pyperclip
- Additional dependencies in `requirements.txt`

## 🛠️ Installation

### Web Version Setup

1. **Install Docker** (if not already installed):
   - [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/)
   - [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
   - [Docker for Linux](https://docs.docker.com/engine/install/)

2. **Clone and run**:
   ```bash
   git clone <repository-url>
   cd HelperApp
   chmod +x run-docker.sh
   ./run-docker.sh
   ```

3. **Access the application** at `http://localhost:8080`

### Desktop Version Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HelperApp
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### Web Application

The web interface provides all functionality through a modern browser-based UI:

1. **Log Check Tab**: Record new log checks with timestamps and outcomes
2. **History Tab**: View, export, and manage previous checks
3. **AWS Queries Tab**: Access pre-built queries with copy-to-clipboard functionality
4. **Evidence Pack Tab**: Generate professional documentation with dynamic sections

### Desktop Application

The desktop version offers the same features with native system integration:

- **System notifications** for reminders
- **Native file dialogs** for exports and imports
- **System tray integration** (where supported)
- **Keyboard shortcuts** and native UI elements

## 🏗️ Application Structure

```
HelperApp/
├── main.py                 # Desktop application entry point
├── web_app.py             # Web application entry point
├── gui.py                 # Desktop GUI components
├── database.py            # Database management
├── reminder.py            # Reminder system
├── evidence_pack_tab.py   # Evidence pack generator (desktop)
├── config.py              # Application configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── run-docker.sh          # Docker runner script
├── templates/
│   └── index.html         # Web interface template
└── data/                  # Database storage directory
```

## 🔧 Configuration

### Database Configuration

Both versions use SQLite for data storage:
- **Web version**: `/home/appuser/app/data/` (in container)
- **Desktop version**: `./data/` (local directory)

### Reminder Settings (Desktop Only)

Configure automatic check reminders in the Settings tab:
- Enable/disable reminders
- Set reminder intervals (1-168 hours)
- Customize reminder messages

## 📊 Evidence Pack Generation

Generate professional evidence documentation with:

### Basic Information
- Date/time of check
- Checker name
- Environment (Production/Staging/Development)
- AWS account details

### Log Sources
- CloudWatch Logs
- CloudTrail
- Application Logs
- Security Logs (WAF, GuardDuty, etc.)

### Dynamic Sections
- **Findings**: Add/remove findings with descriptions
- **Actions Taken**: Document remediation steps
- **Follow-up Required**: Track outstanding items with due dates
- **Screenshots/Evidence**: Reference supporting materials

### Sign-off
- Checked by
- Reviewed by
- Completion date

## 🔍 AWS Query Library

Pre-built queries for common scenarios:

### CloudWatch Insights
- Error detection patterns
- Performance monitoring
- Memory usage analysis
- Custom log parsing

### AWS CLI Commands
- CloudTrail failed login detection
- SSM session history
- Security event queries
- Resource utilization checks

## 🐳 Docker Deployment

### Local Development
```bash
docker build -t aws-log-helper .
docker run -p 8080:8080 aws-log-helper
```

### Production Deployment
```bash
# With persistent data storage
docker run -d \
  --name aws-log-helper \
  -p 8080:8080 \
  -v $(pwd)/data:/home/appuser/app/data \
  aws-log-helper
```

### Cloud Deployment

The web version can be deployed to any cloud platform that supports Docker:

- **AWS**: ECS, Fargate, or EC2
- **Google Cloud**: Cloud Run or GKE
- **Azure**: Container Instances or AKS
- **Heroku**: Container registry
- **DigitalOcean**: App Platform

## 📤 Data Export

### Export Formats
- **CSV**: Full history export for analysis
- **Evidence Packs**: Formatted documentation ready for sharing
- **Database Backup**: Complete data backup for migration

### Export Options
- **Web version**: Download through browser
- **Desktop version**: Save to local filesystem

## 🔒 Security

### Web Application
- Non-root user execution in container
- No network access to host system
- Isolated data storage
- Input validation and sanitization

### Desktop Application
- Local data storage only
- No network communications (except for updates)
- User-controlled data access

## 🛠️ Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both web and desktop versions
5. Submit a pull request

### Running Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Building Executables

For desktop distribution:
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --windowed --onefile main.py
```

## 📝 Changelog

### Version 2.0.0
- Added cross-platform web interface
- Docker containerization
- Improved evidence pack generation
- Enhanced UI with modern dark theme
- Better mousewheel scrolling support

### Version 1.0.0
- Initial desktop GUI release
- Basic log tracking functionality
- Evidence pack generation
- AWS query library

## 🆘 Troubleshooting

### Web Version Issues
- **Can't access localhost:8080**: Ensure Docker is running and port is not in use
- **Container won't start**: Check Docker logs with `docker logs <container-id>`
- **Data persistence**: Ensure proper volume mounting for data directory

### Desktop Version Issues
- **Import errors**: Install missing dependencies with `pip install -r requirements.txt`
- **GUI not showing**: Ensure tkinter is installed and DISPLAY is set (Linux)
- **macOS button visibility**: Update to latest version with improved button styling

### Common Issues
- **Database errors**: Check file permissions in data directory
- **Performance issues**: Consider cleaning old records or increasing system resources

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include logs and system information

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- Built with Python and modern web technologies
- Uses CustomTkinter for enhanced desktop UI
- Flask for web application framework
- Docker for cross-platform deployment