// pages/api/networkx/index.js

import { exec } from 'child_process';
import { NextResponse } from 'next/server';
import path from 'path';
import { promisify } from 'util';
const execAsync = promisify(exec);

// define path to python folder
const pythonFolder = '_py'; 

// get base path
const cwd = process.cwd();

// get base path
const basePath = cwd.split('app')[0];

// get path to run python script
const pythonPath = path.join(basePath, pythonFolder, 'neogds.sh');

async function runPython() {
  try {
    // Replace 'python' with the path to your Python executable if needed
    const { stdout, stderr } = await execAsync(pythonPath);
    if (stderr) {
      throw new Error(stderr);
    }
    const jsonData = JSON.parse(stdout);
    return jsonData;
  } catch (error) {
    console.error('Error executing Python script:', error);
    return { error: 'Failed to run Python script' };
  }
}

export async function GET(req, res) {
  
  const jsonData = await runPython();
  return NextResponse.json(jsonData);

}
