#![feature(duration_as_u128)]

use std::{
    fs::File,
    io::{BufRead, BufReader, Error},
    result::Result,
    time::Instant,
};

use rand::{thread_rng, Rng};

static LARGE_SIZES: [u32; 10] = [
    5000, 10000, 20000, 25000, 50000, 100000, 200000, 500000, 1000000, 2000000,
];
static SIZES: [u32; 10] = [100, 250, 500, 1000, 2500, 5000, 10000, 12500, 15000, 20000];

fn main() {
    let mut arrays: Vec<Vec<u32>> = LARGE_SIZES
        .iter()
        .map(|size| generate_data(*size))
        .collect();

    println!("===Sorting with four-way merge sort===");

    arrays.iter().for_each(|arr| {
        let before = Instant::now();
        let arr = four_way_merge_sort(arr);
        let after = Instant::now();
        let diff = after.duration_since(before);
        verify(&arr);
        println!("[{} Elements] {}ms", arr.len(), diff.as_millis());
    });

    println!("===Sorting with build-in sort===");

    arrays.iter_mut().for_each(|arr| {
        let before = Instant::now();
        arr.sort();
        let after = Instant::now();
        let diff = after.duration_since(before);
        verify(&arr);
        println!("[{} Elements] {}ms", arr.len(), diff.as_millis());
    });
}

fn verify(list: &[u32]) {
    for i in 0..(list.len() - 1) {
        assert!(list[i] <= list[i + 1]);
    }
}

fn insertion_sort(list: &mut Vec<u32>) {
    for idx in 1..list.len() {
        let stored = list[idx];
        let mut pos = idx;
        while pos > 0 && list[pos - 1] > stored {
            list[pos] = list[pos - 1];
            pos -= 1;
        }

        list[pos] = stored;
    }
}

fn four_way_merge_sort(list: &[u32]) -> Vec<u32> {
    if list.len() > 1 {
        let middle = list.len() / 2;

        let (left, right) = list.split_at(middle);
        let (far_left, left) = left.split_at(left.len() / 2);
        let (right, far_right) = right.split_at(right.len() / 2);

        let far_left = four_way_merge_sort(far_left);
        let left = four_way_merge_sort(left);
        let right = four_way_merge_sort(right);
        let far_right = four_way_merge_sort(far_right);

        let left = merge(&left, &far_left);
        let right = merge(&right, &far_right);
        return merge(&left, &right);
    }

    list.to_vec()
}

fn merge(left: &[u32], right: &[u32]) -> Vec<u32> {
    let mut leftc = 0;
    let mut rightc = 0;

    let mut dest = Vec::with_capacity(left.len() + right.len());

    while leftc < left.len() && rightc < right.len() {
        if left[leftc] < right[rightc] {
            dest.push(left[leftc]);
            leftc += 1;
        } else {
            dest.push(right[rightc]);
            rightc += 1;
        }
    }

    while leftc < left.len() {
        dest.push(left[leftc]);
        leftc+=1;
    }

    while rightc < right.len() {
        dest.push(right[rightc]);
        rightc+=1;
    }

    dest
}

fn load_file() -> Result<Vec<Vec<u32>>, Error> {
    let reader = BufReader::new(File::open("data.txt")?);

    let data: Vec<_> = reader
        .lines()
        .filter_map(|x| x.ok())
        .map(|line| {
            line.split(' ')
                .skip(1)
                .filter_map(|val| val.parse::<u32>().ok())
                .collect::<Vec<_>>()
        })
        .collect();

    Ok(data)
}

fn generate_data(size: u32) -> Vec<u32> {
    let mut rng = thread_rng();
    (0..size).map(|_| rng.gen::<u32>() % 10_000).collect()
}
