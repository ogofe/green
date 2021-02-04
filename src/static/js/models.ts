interface Client{
    first_name: string,
    last_name: string,
    card: null,
    country: string
}


interface Card{
    client: null,
    name_on_card: string,
    card_number: string,
    card_cvv: string,
    card_type: string,
    exp: string,
}

declare var Client: {
    new() : Client;
    prototype: Client;
}

declare var Card: {
    new() : Card;
    prototype: Card;
}

