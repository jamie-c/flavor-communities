import path from 'path';

// define path to python folder
const pythonFolder = '_py'; 
// get base path
const cwd = process.cwd();


export function setPath(fileName) {
    return path.join(cwd, 'src', pythonFolder, fileName);    
}