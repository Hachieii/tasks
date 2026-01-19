const express = require("express");
const dayjs = require("dayjs");
const sqlite3 = require("sqlite3");
const assert = require("node:assert");
const { error } = require("node:console");

const db = new sqlite3.Database("./database.db");
const app = express();
const port = 3000;

const init = `
CREATE TABLE IF NOT EXISTS logger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ip_address TEXT,
  user_agent TEXT,
  referer TEXT,
  url TEXT,
  cookie TEXT,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS flag (
  id INTEGER PRIMARY KEY UNIQUE,
  secret TEXT NOT NULL UNIQUE
);

INSERT INTO flag (id, secret) VALUES (1, 'KCSC{ehehe}');
`;

db.serialize(() => {
  db.exec(init, (err) => {
    console.log(err ? err : "Tables created");
    assert(err);
  });
});

app.use((req, res) => {
  const ip_address = req.ip;
  const user_agent = req.headers["user-agent"];
  const referer = req.headers["referer"];
  const url = `${req.protocol}://${req.get("host")}${req.originalUrl}`;
  const cookie = req.headers["cookie"];
  const created_at = dayjs().format("YYYY-MM-DD HH:mm:ss.SSSSSS");

  console.log(
    `ip: ${ip_address} \nuser_agent: ${user_agent} \nreferer: ${referer} \nurl: ${url} \ncookie: ${cookie} \ncreated_at: ${created_at}`,
  );

  db.run(
    `INSERT INTO logger (ip_address, user_agent, referer, url, cookie, created_at) VALUES ('${ip_address}', '${user_agent}', '${referer}', '${url}', '${cookie}', '${created_at}'
  )`,
    (err) => {
      res.send(err ? "Error" : "Logged");
      console.log(err);
    },
  );
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
