#!/usr/bin/env node
import { spawnSync, spawn } from "child_process";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pythonServer = join(__dirname, "server.py");
const requirements = join(__dirname, "requirements.txt");

// Make sure dependencies are installed
console.error("Installing Python dependencies...");
spawnSync("pip", ["install", "-r", requirements, "-q"], { stdio: ["ignore", "ignore", "inherit"] });


// Pass all command-line args to the Python server
const args = process.argv.slice(2);
console.error("Starting FastMCP server...");

const child = spawn("python", [pythonServer, ...args], { stdio: "inherit" });
child.on("exit", (code) => process.exit(code));
