use core::ops::{Deref, DerefMut};
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::result::Result;

fn main() -> Result<(), Box<Error>> {
    //Load the data
    let mut activities: ActivitySet = File::open("./act.txt")?.into();

    //Create a result container
    let mut results: ActivitySet = ActivitySet(vec![]);

    //For every entry in our list of activities
    for ac_list in activities.iter_mut() {
        //Sort by the starting time
        ac_list.sort_by_key(|itm| itm.start);
        //Reverse, so the highest starting time is first
        ac_list.reverse();
        //Grab the first item for comparison
        let first = *ac_list.first().unwrap();
        //Create a new list from our activity list
        let new_list = ac_list
            .iter_mut()
            //We always add the first, so skip that one
            .skip(1)
            //Fold down our activities
            .fold(vec![first], |mut acc: Vec<Activity>, itm| {
                //Grab the most recent activity out of the list
                if let Some(last) = acc.last() {
                    //If the one we're looking at currently ends at or before the most recent one begins
                    if last.start >= itm.end {
                        //Add it to our list of items
                        acc.push(*itm)
                    }
                }

                //Return our list of items for use in the next iteration
                acc
            });

        //Add our new list of activities (that don't overlap) to the list of results
        results.push(new_list);
    }

    print_results(results);

    Ok(())
}

fn print_results(results: ActivitySet) {
    for (idx, result) in results.iter().enumerate() {
        println!(
            "Set: {}\nNumber of Activities Selected: {}\nActivities: {}",
            idx + 1,
            result.len(),
            result
                .iter()
                .rev()
                .map(|activity| format!("{}", activity.num))
                .collect::<Vec<_>>()
                .join(" ")
        )
    }
}

#[derive(Debug, Copy, Clone)]
struct Activity {
    num: u32,
    start: u32,
    end: u32,
}

//Container struct so that we can implement traits like `From<T>` onto Vec<Vec<Activity>>
#[derive(Debug, Clone)]
struct ActivitySet(Vec<Vec<Activity>>);

impl Deref for ActivitySet {
    type Target = Vec<Vec<Activity>>;

    fn deref(&self) -> &Vec<Vec<Activity>> {
        &self.0
    }
}

impl DerefMut for ActivitySet {
    fn deref_mut(&mut self) -> &mut Vec<Vec<Activity>> {
        &mut self.0
    }
}

//File parsing. Feel free to read, but totally unrelated to the algorithm
//Implementing this trait is what allows us to use the `.into()` function for conversion
impl From<File> for ActivitySet {
    fn from(file: File) -> Self {
        //Make a buffer to store our activities once they're parsed
        let mut activities: Vec<Vec<Activity>> = vec![];

        //Create a buffered reader, which allows for splitting the file by .lines()
        let reader = BufReader::new(file);

        //For every line
        for line in reader.lines().filter_map(Result::ok) {
            //Now we split our parts into an iterator
            let parts: Vec<u32> = line
                .split(" ")
                .into_iter()
                //Parse each number in this line into unsigned 32 bit ints, and panic if it fails
                .filter_map(|part| part.parse().ok())
                //Collect the iterator of converted values back into an array
                .collect();

            //If we're not looking at a data line
            if parts.len() < 3 {
                if let Some(first) = parts.first() {
                    activities.push(Vec::with_capacity(*first as usize));
                }

                continue;
            }

            //Add a new activity from the parts we've parsed earlier
            if let Some(last) = activities.last_mut() {
                if let (Some(&num), Some(&start), Some(&end)) =
                    (parts.get(0), parts.get(1), parts.get(2))
                {
                    last.push(Activity { num, start, end });
                }
            }
        }

        //Return our set of activities in the order of when they were parsed
        ActivitySet(activities)
    }
}
