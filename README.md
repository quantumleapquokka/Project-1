# LConnect v.01
### Development Timeline: 

#Phase 1: Project Setup

**Goal:** Prepare development environment and initial project structure.

### ✅ Tasks
- [ ] Install Python 3.8+
- [ ] Install libraries:
  - `ftplib`
  - `requests`
  - `PyQt5` or `tkinter`
  - `yaml` or `json`
  - `cryptography`
- [ ] Create folder structure:
- LConnect/
- ├── config/
- │ └── config.yaml
- ├── core/
- │ ├── ftp_handler.py
- │ ├── api_handler.py
- │ ├── logger.py
- ├── ui/
- │ └── main_ui.py
- ├── utils/
- │ └── encryption.py
- ├── data/
- │ └── positives/
- ├── logs/
- └── main.py

---

## 🔄 Phase 2: Core Functionality

**Goal:** Enable image polling, processing, and logging.

### ✅ Tasks
- [ ] **FTP Polling (`ftp_handler.py`)**
- Connect using credentials
- Check for and download new image files
- Mark images as processed
- [ ] **API Submission (`api_handler.py`)**
- Send image via HTTP POST
- Parse JSON response
- [ ] **Positive Detection Handling**
- Save flagged images to `data/positives/` with timestamps
- [ ] **Logging (`logger.py`)**
- Log timestamp, image name, folder, response code, detection result

---

## 🖥️ Phase 3: GUI Implementation

**Goal:** Create user-friendly config & monitoring interface.

### ✅ Tasks
- [ ] **UI Elements (`main_ui.py`)**
- Folder-to-API mapping table (add/edit/delete)
- Start/Stop button
- Display last run time, error count, recent errors
- [ ] **Backend Integration**
- Link GUI actions to config and polling logic
- Validate inputs before saving

---

## Phase 4: Configuration Management

**Goal:** Store and persist settings.

### ✅ Tasks
- [ ] Store FTP credentials, folder mappings, polling interval in YAML/JSON
- [ ] Read/write config from file with validation

---

## Phase 5: Error Handling

**Goal:** Improve fault tolerance and error visibility.

### ✅ Tasks
- [ ] Implement retry logic (up to 3 times) on FTP/API failure
- [ ] Catch and log exceptions
- [ ] Display last 10 errors in the GUI

---

##  Phase 6: Security

**Goal:** Secure sensitive information.

### ✅ Tasks
- [ ] Encrypt credentials using AES-256 (`encryption.py`)
- [ ] Optionally prompt for a master password
- [ ] Use FTPS/SFTP and HTTPS for secure transfers

---

##  Phase 7: Performance Tuning & Testing

**Goal:** Ensure responsiveness and reliability.

### ✅ Tasks
- [ ] Ensure image processing <3s per image
- [ ] Maintain idle memory usage <50MB
- [ ] Write unit tests for:
- FTP connectivity
- API integration
- Config read/write validation

---

##  Phase 8: Validation & Packaging

**Goal:** Final testing and deployment prep.

### ✅ Tasks
- [ ] Test with mock FTP and API endpoints
- [ ] Package with `pyinstaller` or similar
- [ ] Write setup and installation guide

---

##  Optional Enhancements (Stretch Goals)

- [ ] UI tab for viewing logs
- [ ] System tray icon integration
- [ ] Run as background service or scheduled task

---

> Designed for wildfire detection workflows, built with reliability and simplicity in mind.
