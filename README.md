# apokentromena

1️⃣ Τι είναι το project με μια πρόταση

Το project ζητά:

Να υλοποιήσεις και να συγκρίνεις πειραματικά δύο Distributed Hash Tables (DHTs): Chord και Pastry, χρησιμοποιώντας πραγματικά ή συνθετικά δεδομένα, και να μετρήσεις την απόδοσή τους σε βασικές λειτουργίες.

Δεν είναι θεωρητικό — είναι καθαρά υλοποίηση + πειράματα.

2️⃣ Τι συστήματα πρέπει να υλοποιήσεις

Πρέπει να υλοποιήσεις δύο P2P υποδομές:

🔹 Chord DHT

Δακτύλιος (ring)
Consistent hashing
Finger tables
Routing μέσω hops

🔹 Pastry DHT

Prefix-based routing
Routing tables
Leaf sets
Neighborhood sets

👉 Δεν αρκεί να τα περιγράψεις. Πρέπει να δουλεύουν (έστω σε προσομοίωση).

3️⃣ Ποιες βασικές διαδικασίες (operations) ζητούνται
Για κάθε DHT (Chord & Pastry) πρέπει να υλοποιήσεις και να μετρήσεις:

🔧 Βασικές λειτουργίες δεδομένων

Build
Αρχικοποίηση του δικτύου
Δημιουργία κόμβων (peers)

Insert(key, value)
Εισαγωγή εγγραφής (movie)

Delete(key)
Διαγραφή εγγραφής

Update(key, value)
Ενημέρωση εγγραφής

Lookup(key)
Αναζήτηση με βάση το key (exact match)

🌐 Λειτουργίες δικτύου

Node Join
Νέος κόμβος μπαίνει στο DHT

Node Leave
Κόμβος αποχωρεί (graceful ή όχι)

Για κάθε μία πρέπει να:
λειτουργεί σωστά
μετράς αριθμό hops

4️⃣ Τι θεωρείται key και τι value
🔑 Key

Τίτλος ταινίας (title)

key = hash(movie_title)

📦 Value

Τα υπόλοιπα attributes της ταινίας (14 διαστάσεις):

genre
budget
revenue
popularity
vote_average
κ.λπ.

Δηλαδή:
(key, value) = (title, {attributes})

5️⃣ Dataset – πώς χρησιμοποιείται

Προτείνεται (όχι υποχρεωτικά):
Movies Metadata Dataset (Kaggle) 
Project1-DHTs-2025(En)[100%]
~946.000 ταινίες
14 attributes

Τι κάνεις εσύ:
Διαβάζεις το CSV
Παίρνεις υποσύνολο (π.χ. 10k, 50k records)
Κάνεις hash το title
Αποθηκεύεις την ταινία στο DHT

💡 Δεν χρειάζεται να φορτώσεις όλο το dataset αν δεν αντέχει το σύστημα.

6️⃣ Ειδικό ερώτημα που ζητείται (K-movies popularity)

Ζητείται ρητά:
Να εντοπίζονται ταυτόχρονα (concurrently) οι popularities των K ταινιών με τίτλους:
title-1, title-2, …, title-K

Τι σημαίνει πρακτικά:
Δίνεις K τίτλους
Κάνεις K lookup queries

Μετράς:
hops
χρόνο
Επιστρέφεις το popularity κάθε ταινίας

📌 Μπορεί να γίνει:

με threads
ή σειριακά (αν θες απλούστερη υλοποίηση)

7️⃣ Τοπικά indexes (bonus αλλά σημαντικό)

Αφού βρεις τον σωστό peer:
Τα δεδομένα είναι τοπικά

Εκεί μπορείς να χρησιμοποιήσεις:
B+ tree
hash table
sorted list

Αυτό δεν είναι το κύριο ζητούμενο, αλλά δείχνει καλή αρχιτεκτονική.

8️⃣ Τι μετρήσεις (experiments) πρέπει να κάνεις

Για Chord vs Pastry:
📊 Μετρήσεις
Αριθμός hops:

Insert
Lookup
Delete
Node join
Node leave

📈 Αποτελέσματα

Γραφήματα:
hops vs αριθμός κόμβων
σύγκριση Chord–Pastry
Πίνακες με averages

⚠️ Αυτό είναι βασικό κομμάτι της βαθμολόγησης

9️⃣ Τι ΔΕΝ ζητείται (για να μην αγχωθείς)

❌ Δεν ζητείται:

Full-scale distributed cloud (Docker/K8s είναι προαιρετικά)
Τέλειο fault tolerance
Production-ready σύστημα

✅ Αρκεί:

σωστή λογική
σωστή μέτρηση hops
καθαρή σύγκριση

🔟 Παραδοτέο (Deliverable)

Πρέπει να δώσεις:
Zip/Rar
Εκτελέσιμα αρχεία
Κώδικα
(καλό να έχεις και README)

Deadline: 1-2η εβδομάδα Φεβρουαρίου
========================================================================================================================================================================================================================================================================================================================================================================================================================================

Εκτέλεση Project:

Πώς τρέχει το project;
Τρέχεις την main του branch zogo και επιλέγεις:
1️⃣ CHORD:
Loading Dataset...
Choose DHT (chord / pastry): chord
Building chord network with 100 nodes...
Chord Network built with 100 nodes (m=16).
INSERT | avg hops=4.000 | time=0.003s
LOOKUP | avg hops=4.000 | time=0.000s

=== Concurrent Popularity Lookup ===
01. Ultimate G's: Zac's Flying Dream                             | popularity: 4.4791
02. How Proust Can Change Your Life                              | popularity: 3.7264
03. Jimmy Neutron: Operation: Rescue Jet Fusion                  | popularity: 5.2546
04. Pass The Mic!                                                | popularity: 3.4843
05. Harvesting Horror: Children of the Corn                      | popularity: 4.092
06. Barbecue: A Texas Love Story                                 | popularity: 4.0708
07. The Making of 'Heat'                                         | popularity: 3.0967
08. Proteus: A Nineteenth Century Vision                         | popularity: 3.2603
09. Ice Cube: The Making of a Don                                | popularity: 3.7178
10. Aberfan: The Untold Story                                    | popularity: 3.1212
11. The Damned Thing                                             | popularity: 3.8826
12. A Very Fairy Christmas                                       | popularity: 3.1437
13. Spider's Web: A Pig's Tale                                   | popularity: 3.0996
14. Zygon                                                        | popularity: 5.9232
15. Darwin's Struggle: The Evolution of the Origin of Species    | popularity: 3.3112
16. Maya Deren's Sink                                            | popularity: 4.0014
17. Pulse                                                        | popularity: 3.2874
18. Dive, Dive, Dive! with Robert Llewellyn                      | popularity: 3.5646
19. Quiet                                                        | popularity: 3.7397
20. The Evil Dead Inbred Rednecks                                | popularity: 3.0755
21. Reboot                                                       | popularity: 4.0698
22. Mel Smith: I've Done Some Things                             | popularity: 3.7676
23. River Deep, Mountain High: James Nesbitt in New Zealand      | popularity: 3.5209
24. The 10 Faces of Michael Jackson                              | popularity: 3.035
25. Bring Me the Head of Tim Horton                              | popularity: 3.8122
26. The Keys of Christmas                                        | popularity: 3.0808
27. Rodney King                                                  | popularity: 4.6035
28. The Private War of Joseph Sargent                            | popularity: 4.4762
29. Russia 1917: Countdown to Revolution                         | popularity: 3.1116
30. On the Line: The Race of Champions                           | popularity: 4.5074
DELETE | avg hops=3.871 | time=0.000s
JOIN   | avg hops=4.516 | time=0.006s
LEAVE  | avg hops=2.742 | time=0.006s

Process finished with exit code 0

2️⃣ PASTRY:
Loading Dataset...
Choose DHT (chord / pastry): pastry
Building pastry network with 100 nodes...
Pastry Network built with 100 nodes.
INSERT | avg hops=1.484 | time=0.002s
LOOKUP | avg hops=1.613 | time=0.000s

=== Concurrent Popularity Lookup ===
01. Ultimate G's: Zac's Flying Dream                             | popularity: 4.4791
02. How Proust Can Change Your Life                              | popularity: 3.7264
03. Jimmy Neutron: Operation: Rescue Jet Fusion                  | popularity: 5.2546
04. Pass The Mic!                                                | popularity: 3.4843
05. Harvesting Horror: Children of the Corn                      | popularity: 4.092
06. Barbecue: A Texas Love Story                                 | popularity: 4.0708
07. The Making of 'Heat'                                         | popularity: 3.0967
08. Proteus: A Nineteenth Century Vision                         | popularity: 3.2603
09. Ice Cube: The Making of a Don                                | popularity: 3.7178
10. Aberfan: The Untold Story                                    | popularity: 3.1212
11. The Damned Thing                                             | popularity: 3.8826
12. A Very Fairy Christmas                                       | popularity: 3.1437
13. Spider's Web: A Pig's Tale                                   | popularity: 3.0996
14. Zygon                                                        | popularity: 5.9232
15. Darwin's Struggle: The Evolution of the Origin of Species    | popularity: 3.3112
16. Maya Deren's Sink                                            | popularity: 4.0014
17. Pulse                                                        | popularity: 3.2874
18. Dive, Dive, Dive! with Robert Llewellyn                      | popularity: 3.5646
19. Quiet                                                        | popularity: 3.7397
20. The Evil Dead Inbred Rednecks                                | popularity: 3.0755
21. Reboot                                                       | popularity: 4.0698
22. Mel Smith: I've Done Some Things                             | popularity: 3.7676
23. River Deep, Mountain High: James Nesbitt in New Zealand      | popularity: 3.5209
24. The 10 Faces of Michael Jackson                              | popularity: 3.035
25. Bring Me the Head of Tim Horton                              | popularity: 3.8122
26. The Keys of Christmas                                        | popularity: 3.0808
27. Rodney King                                                  | popularity: 4.6035
28. The Private War of Joseph Sargent                            | popularity: 4.4762
29. Russia 1917: Countdown to Revolution                         | NOT FOUND | repr='Russia 1917: Countdown to Revolution'
30. On the Line: The Race of Champions                           | popularity: 4.5074
DELETE | avg hops=1.613 | time=0.001s
JOIN   | avg hops=1.548 | time=0.105s
LEAVE  | avg hops=1.548 | time=0.107s

Process finished with exit code 0

▶️ Άνοιξε terminal και γράψε την εξής εντολή για να δεις το plot chrod vs pastry diagram
    python plots/plot_hops.py
