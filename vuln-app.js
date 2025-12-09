// vuln-app.js
// INTENTIONALLY VULNERABLE – DO NOT USE IN PRODUCTION

const express = require("express");
const { exec } = require("child_process");
const mysql = require("mysql2");
const fs = require("fs");
const http = require("http");

const app = express();
app.use(express.json());

// 🔥 Hardcoded DB credentials
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "supersecret",
  database: "testdb",
});

// 🔥 SQL Injection
app.get("/user", (req, res) => {
  const username = req.query.username; // e.g. admin' OR '1'='1
  const query = `SELECT * FROM users WHERE username = '${username}'`; // vulnerable
  connection.query(query, (err, results) => {
    if (err) return res.status(500).send(err.toString());
    res.json(results);
  });
});

// 🔥 Command Injection
app.get("/ping", (req, res) => {
  const host = req.query.host; // e.g. 127.0.0.1 && rm -rf /
  exec(`ping -c 2 ${host}`, (err, stdout, stderr) => {
    if (err) return res.status(500).send(stderr);
    res.send(stdout);
  });
});

// 🔥 Directory Traversal
app.get("/read-file", (req, res) => {
  const file = req.query.file; // e.g. ../../../../etc/passwd
  fs.readFile(file, "utf8", (err, data) => {
    if (err) return res.status(500).send(err.toString());
    res.send(data);
  });
});

// 🔥 Insecure HTTP request (no TLS)
app.get("/proxy", (req, res) => {
  const target = req.query.url || "http://example.com"; // SSRF-ish
  http.get(target, (resp) => {
    let data = "";
    resp.on("data", (chunk) => (data += chunk));
    resp.on("end", () => res.send(data));
  }).on("error", (err) => res.status(500).send(err.toString()));
});

app.listen(3000, () => {
  console.log("Vulnerable app listening on http://localhost:3000");
});
