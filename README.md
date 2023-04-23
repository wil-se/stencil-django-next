# Crypto Casino Backend

# TODO

- [ ] verify email address



# STRUTTURA

| Nome Opzione      | Descrizione                                                                                                        |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| Opzione 1: Web2.5 | L'utente può accedere tramite e-mail/wallet; il saldo viene aggiornato solo in caso di deposito o prelievo.      |
| Opzione 2: Vault  | Il contratto funge da vault senza riferimenti agli utenti; i dettagli degli utenti sono conservati in un database.|
| Opzione 3: Ibrida | Combina elementi delle Opzioni 1 e 2 per offrire un equilibrio tra sicurezza, trasparenza e velocità.            |


| Opzione      | Velocità | Trasparenza | Sicurezza | Difficoltà di sviluppo |
|--------------|----------|-------------|-----------|------------------------|
| Opzione 1    | 70%      | 65%         | 75%       | 60%                    |
| Opzione 2    | 80%      | 60%         | 70%       | 50%                    |
| Opzione 3    | 75%      | 80%         | 85%       | 70%                    |


# Opzione 1: Web2.5
- Questa opzione permette agli utenti di accedere tramite e-mail o wallet e utilizza un sistema in cui il saldo viene aggiornato solo in caso di deposito o prelievo. Ciò può ridurre il carico sulla blockchain, ma potrebbe limitare la trasparenza per gli utenti.
1) utente puo loggarsi con email/wallet
2) farà un deposito inviando soldi ad un nostro contratto con il wallet associato alla mail
3) avrà il suo balance visibile da front end, ma questo balance potrebbe non rispecchiare il balance dell’utente all’interno dello smart contract poiché verrà aggiornato da noi soltanto in caso di withdrawal o di deposito (per evitare di sovraccaricare di richieste la chain ed essere piu veloci e sicuri)
4) non puoi chiedere withdraw se hai una giocata attiva e non puoi aprire una giocata se hai un withdraw in corso
5) il withdrawal potrà essere richiesto anche a wallet diverso da quello con cui hai loggato

# Opzione 2: Vault 
- In questa opzione, il contratto intelligente funge da vault senza riferimenti diretti agli utenti. I dettagli degli utenti sono conservati in un database separato, offrendo una doppia garanzia web2 e web3. Tuttavia, la trasparenza è leggermente inferiore rispetto all'Opzione 3. Il contratto ci serve solo da vault non ce nessun riferimento a chi possiede cosa, lo abbiamo registrato solo noi nel nostro database (blindato ovviamente, e visibile agli utenti), questo ci consente di dare all’utente una doppia garanzia web2 e web3, perche se perde la mail puo loggarsi con wallet e associare una nuova mail, se per il wallet puo accedere a associare una nuova mail, senza creare problemi sulla chain

# Opzione 3: Ibrida 
- L'opzione ibrida combina elementi delle prime due opzioni per offrire un equilibrio tra sicurezza, trasparenza e velocità. Utilizza un sistema di caching per aggiornare i saldi degli utenti e conserva i dettagli degli utenti in un database separato, protetto e criptato.     L'utente può registrarsi e accedere sia tramite e-mail che tramite wallet. L'utente effettua un deposito inviando fondi a un contratto intelligente con il wallet associato all'e-mail. Il saldo dell'utente è visibile nel frontend e viene aggiornato tramite un sistema di caching per ridurre il numero di richieste alla blockchain e migliorare le prestazioni. Il sistema di caching può essere aggiornato periodicamente o in base a eventi specifici (come depositi o prelievi) per garantire che il saldo mostrato sia il più accurato possibile. L'utente non può richiedere un prelievo se ha una giocata attiva e non può iniziare una nuova giocata se ha un prelievo in corso. Il prelievo può essere richiesto anche a un wallet diverso da quello utilizzato per l'accesso, ma è necessario confermare l'identità dell'utente attraverso un processo di verifica per evitare frodi o abusi. Il contratto intelligente funge da vault e mantiene un registro dei saldi degli utenti, ma i dettagli dell'utente (come l'e-mail) sono conservati in un database separato, protetto e criptato. In questo modo, gli utenti possono beneficiare della sicurezza e della trasparenza offerte sia dalla blockchain che dai sistemi Web2. Gli utenti possono collegare o dissociare un indirizzo e-mail o un wallet in qualsiasi momento, a condizione che completino un processo di verifica dell'identità per garantire la sicurezza.
