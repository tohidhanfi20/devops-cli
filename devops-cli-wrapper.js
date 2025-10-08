#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
const mainScriptPath = path.join(__dirname, 'main.py');

const args = [mainScriptPath, ...process.argv.slice(2)];

const pythonProcess = spawn(pythonExecutable, args, {
  stdio: 'inherit'
});

pythonProcess.on('error', (err) => {
  console.error(`Failed to start Python process: ${err}`);
});

pythonProcess.on('close', (code) => {
  if (code !== 0) {
    console.error(`Python process exited with code ${code}`);
  }
});