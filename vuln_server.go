// vuln_server.go
// INTENTIONALLY VULNERABLE – DO NOT USE IN PRODUCTION

package main

import (
	"crypto/md5"
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	db, err := sql.Open("sqlite3", "file:test.db?cache=shared&mode=memory")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	http.HandleFunc("/login", func(w http.ResponseWriter, r *http.Request) {
		user := r.URL.Query().Get("user")
		pass := r.URL.Query().Get("pass")

		// 🔥 SQL Injection
		query := fmt.Sprintf("SELECT * FROM users WHERE username = '%s' AND password = '%s'", user, pass)
		log.Println("Running query:", query)
		rows, err := db.Query(query)
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}
		defer rows.Close()
		fmt.Fprintf(w, "Login query executed\n")
	})

	http.HandleFunc("/exec", func(w http.ResponseWriter, r *http.Request) {
		cmdStr := r.URL.Query().Get("cmd") // e.g. ls; rm -rf /
		// 🔥 Command Injection
		out, err := exec.Command("sh", "-c", cmdStr).CombinedOutput()
		if err != nil {
			http.Error(w, string(out), 500)
			return
		}
		w.Write(out)
	})

	http.HandleFunc("/read", func(w http.ResponseWriter, r *http.Request) {
		path := r.URL.Query().Get("path") // 🔥 Path traversal: ../../etc/passwd
		data, err := ioutil.ReadFile(path)
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}
		w.Write(data)
	})

	http.HandleFunc("/hash", func(w http.ResponseWriter, r *http.Request) {
		password := r.URL.Query().Get("password")
		// 🔥 Weak crypto
		sum := md5.Sum([]byte(password))
		fmt.Fprintf(w, "MD5: %x\n", sum)
	})

	log.Println("Vulnerable Go server listening on :8080")
	http.ListenAndServe(":8080", nil)
}
