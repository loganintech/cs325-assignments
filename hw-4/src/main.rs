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
    for ac_list in activities.0.iter_mut() {
        //Sort by the starting time
        ac_list.sort_by_key(|itm| itm.start);
        //Reverse, so the highest starting time is first
        ac_list.reverse();
        //Grab the first item for comparison
        let first = *ac_list.first().unwrap();
        //Create a new list from our activity list
        let new_list =
            ac_list
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
        results.0.push(new_list);
    }

    print_results(results);

    Ok(())
}

fn print_results(results: ActivitySet) {
    for (idx, result) in results.0.iter().enumerate() {
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


//File parsing. Feel free to read, but totally unrelated to the algorithm
//Implementing this trait is what allows us to use the `.into()` function for conversion
impl From<File> for ActivitySet {
    fn from(file: File) -> Self {
        //Make a buffer to store our activities once they're parsed
        let mut activities: Vec<Vec<Activity>> = vec![];

        //Create a buffered reader, which allows for splitting the file by .lines()
        let reader = BufReader::new(file);

        //Split the file into different lines and make sure they are parsed ok. If they aren't they're discarded
        let lines = reader.lines().filter_map(Result::ok);
        //For every line
        for line in lines {
            //Split it by spaces so lines `1 2 3` become ["1", "2", "3"] and `1` becomes [1]
            let parts: Vec<_> = line.split(" ").collect();

            //If we're not looking at a data line
            if parts.len() != 3 {
                //Extrac the number of activities and parse it into a number which is the number of bits of the current architecture (used for indexing)
                let num = parts[0].parse::<usize>().unwrap();
                //Add the space for our list of activities with pre-determined length (to save memory and allocation time)
                activities.push(Vec::with_capacity(num));
                //And skip to the next line
                continue;
            }

            //Now we split our parts into an iterator
            let parts: Vec<_> = parts
                .into_iter()
                //Parse each number in this line into unsigned 32 bit ints, and panic if it fails
                .map(|x| x.parse::<u32>().unwrap())
                //Collect the iterator of converted values back into an array
                .collect();

            //Get the latest array we're working on building
            let last_index = activities.len() - 1;
            //Add a new activity from the parts we've parsed earlier
            activities[last_index].push(Activity {
                num: parts[0],
                start: parts[1],
                end: parts[2],
            })
        }

        //Return our set of activities in the order of when they were parsed
        ActivitySet(activities)
    }
}
