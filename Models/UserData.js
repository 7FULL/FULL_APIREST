class UserData{
    constructor(contacts, coins, user){
        if (contacts == null) {
            contacts = [];
        }
    
        if (coins == null || coins < 0) {
            coins = -1;
        }

        this.contacts = contacts;
        this.coins = coins;
        this.user = user;
    }

    addContact(contact){
        this.contacts.push(contact);
    }

    removeContact(contact){
        const index = this.contacts.indexOf(contact);

        if (index > -1) {
            this.contacts.splice(index, 1);
        }
    }
}

module.exports = UserData;