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
    // ruleid: handler-attribute-read-from-multiple-sources
    session, err := store.Get(r, "blah-session")
    user_id := session.user_id

    if !ValidateUser(user_id) {
        http.Error(w, "Error", http.StatusInternalServerError)
        return
    }

    user_id = r.query.params.user_id
    user_obj := RetrieveUser(user_id)
    user_obj.account_id = r.query.params.account_id
    user_obj.save()
}

func MyHandlerDict(w http.ResponseWriter, r *http.Request) {
    // ruleid: handler-attribute-read-from-multiple-sources-dict
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

func main() {
    http.HandleFunc("/account", MyHandler)

    http.ListenAndServe(":8080", nil)
}

