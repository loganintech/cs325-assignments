echo "===Untimed Merge Sort==="
python3 ./merge.py
echo "==Output of Merge.py=="
cat ./merge.txt
echo "===Untimed Insertion Sort==="
python3 ./insert.py
echo "==Output of Insert.py=="
cat ./insertion.txt

echo "===Timed Merge Sort==="
python3 ./mergeTime.py
echo "===Timed Insertion Sort==="
python3 ./insertTime.py
