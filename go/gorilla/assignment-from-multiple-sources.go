package main
import (
    "net/http"
    "github.com/gorilla/sessions"
)

type User struct {
    user_id int
    account_id string
}
    

func ValidateUser(user_id int) bool {
    return true
}

func RetrieveUser(user_id int) User {
    return User{user_id, "0000"}
}

var store = sessions.NewCookieStore([]byte("blah-blah-blah"))

func MyHandler(w http.ResponseWriter, r *http.Request) {
    // ruleid: assignment-from-multiple-sources
    session, err := store.Get(r, "blah-session")
    user_id := session.Values["user_id"]

    if !ValidateUser(user_id) {
        http.Error(w, "Error", http.StatusInternalServerError)
        return
    }

    user_id = r.query.params.user_id
    user_obj := RetrieveUser(user_id)
    user_obj.account_id = r.query.params.account_id
    user_obj.save()
}

func MyHandlerNoWalus(w http.ResponseWriter, r *http.Request) {
    // ruleid: assignment-from-multiple-sources-no-walrus
    session, err := store.Get(r, "blah-session")
    var user_id int = session.Values["user_id"].(int)

    if !ValidateUser(user_id) {
        http.Error(w, "Error", http.StatusInternalServerError)
        return
    }

    user_id = r.query.params.user_id
    user_obj := RetrieveUser(user_id)
    user_obj.account_id = r.query.params.account_id
    user_obj.save()
}

func main() {
    http.HandleFunc("/account", MyHandler)

    http.ListenAndServe(":8080", nil)
}
