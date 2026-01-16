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