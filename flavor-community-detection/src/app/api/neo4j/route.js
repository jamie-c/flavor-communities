// pages/api/networkx/index.js

import { setPath } from '@/app/utils/setPath';
import { exec } from 'child_process';
import { NextResponse } from 'next/server';
import { promisify } from 'util';
const execAsync = promisify(exec);

// define shell script to run python script
const shellScript = 'neog.sh';

// set path to run python script (via the shell script)
const pythonPath = setPath(shellScript);

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
