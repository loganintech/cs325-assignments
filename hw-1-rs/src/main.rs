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

    for arr in arrays.iter_mut() {
        let before = Instant::now();
        merge_sort(arr);
        let after = Instant::now();
        let diff = after.duration_since(before);
        println!("[{} Elements] {}ms", arr.len(), diff.as_millis());
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

fn merge_sort(list: &mut [u32]) {
    if list.len() > 1 {
        let middle = list.len() / 2;

        let (left, right) = list.split_at_mut(middle);
        merge_sort(left);
        merge_sort(right);
        merge(left, right);
    }
}

fn merge(left: &mut [u32], right: &mut [u32]) -> Vec<u32> {
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
