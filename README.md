# BVSPiLogger

**BV**iLogger** is a Raspberry Pi-based environmental monitoring platform designed for automated sensor deployment, environmental data collection, and long-term data logging.

Built around the Pimoroni WeatherHAT ecosystem, the platform enables researchers, educators, and hobbyists to rapidly deploy low-cost environmental monitoring systems capable of recording temperature, humidity, pressure, and light measurements.

The project was developed to simplify hardware deployment, automate configuration, and create reproducible environmental monitoring workflows.

---

## Key Features

### Environmental Monitoring

- Temperature measurement
- Relative humidity monitoring
- Atmospheric pressure recording
- Light intensity sensing
- Automated timestamping

### Automated Deployment

- Raspberry Pi setup automation
- WeatherHAT installation and configuration
- Automatic dependency installation
- I2C and SPI configuration

### Data Logging

- Continuous environmental monitoring
- CSV data export
- Longitudinal data collection
- Lightweight storage requirements

### Network Configuration

- Eduroam deployment support
- Automated wireless setup workflows
- Rapid deployment to new devices

### Raspberry Pi Integration

- WeatherHAT support
- Linux-based deployment
- Automated startup configuration
- Sensor hardware management

---

## Technology Stack

- Python
- Raspberry Pi OS
- Pimoroni WeatherHAT
- CSV Data Logging
- Linux Automation
- Cron Scheduling

---

## Installation

Clone the repository:

```bash
git clone https://github.com/DrRichBruce/PiLogger.git

cd PiLogger
```

Run the installation script:

```bash
python3 weather-pi-setup.py
```

After configuration and reboot:

```bash
python3 weather-pi-run.py
```

---

## Repository Structure

```text
BVSPiLogger

├── weather-pi-setup.py
├── weather-pi-setup-new.py
├── weather-pi-run.py
├── weather-pi-demo.py
└── eduroam-setup.py
```

---

## Use Cases

BVSPiLogger is intended to support:

- Environmental monitoring
- Field sensor deployments
- Educational STEM projects
- Raspberry Pi development
- Data logging applications
- Weather observation projects
- Research support workflows
- IoT prototyping

---

## Design Principles

BVSPiLogger is based on several core principles:

- Low-cost environmental monitoring
- Rapid hardware deployment
- Reproducible setup workflows
- Minimal configuration requirements
- Accessible hardware and software
- Reliable long-term data collection

The goal is to reduce technical barriers to environmental monitoring while maintaining flexibility for researchers and makers.

---

## Future Development

Planned enhancements include:

- Real-time dashboard visualisation
- Database integration
- Remote monitoring interfaces
- Automated plotting and reporting
- Cloud synchronisation
- Additional environmental sensors
- Wireless telemetry support

---

## Author

**Dr Richard Bruce**

Research Project Officer  
Bristol Veterinary School

### Interests


- Computational Biology
- Transcriptomics
- AI for Life Sciences
- Data Science
- Scientific Software Development


---

## Project Origins

BVSPiLogger was developed to simplify the deployment of Raspberry Pi-based environmental monitoring systems. The project evolved through iterative improvements in deployment automation, sensor integration, network configuration, and data collection workflows, ultimately becoming a reusable platform for environmental sensing and lightweight field monitoring.
