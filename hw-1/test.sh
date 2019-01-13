echo "===Untimed Merge Sort==="
python3 ./mergesort.py
echo "==Output of Mergesort.py=="
cat ./merge.txt
echo "===Untimed Insertion Sort==="
python3 ./insertsort.py
echo "==Output of Insertsort.py=="
cat ./insertion.txt

echo "===Timed Merge Sort==="
python3 ./mergeTime.py
echo "===Timed Insertion Sort==="
python3 ./insertTime.py
