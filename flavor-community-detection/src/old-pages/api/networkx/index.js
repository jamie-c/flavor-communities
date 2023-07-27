// pages/api/networkx/index.js

import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);

export default async function handler(req, res) {
  try {
    // Replace 'python' with the path to your Python executable if needed
    const { stdout, stderr } = await execAsync('$WORKON_HOME/exaptive/exaptive/flavor-community-detection/src/_py/netx.sh');
    if (stderr) {
      throw new Error(stderr);
    }
    const jsonData = JSON.parse(stdout);
    res.status(200).json(jsonData);
  } catch (error) {
    console.error('Error executing Python script:', error);
    res.status(500).json({ error: 'Failed to run Python script' });
  }
}
