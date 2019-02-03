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
        let mut activities: Vec<Vec<Activity>> = vec![];

        let reader = BufReader::new(file);

        let lines = reader.lines().filter_map(Result::ok);
        for line in lines {
            let parts: Vec<_> = line.split(" ").collect();

            if parts.len() != 3 {
                let num = parts[0].parse::<usize>().unwrap();
                activities.push(Vec::with_capacity(num));
                continue;
            }

            let parts: Vec<_> = parts
                .into_iter()
                .map(|x| x.parse::<u32>().unwrap())
                .collect();

            let last_index = activities.len() - 1;
            activities[last_index].push(Activity {
                num: parts[0],
                start: parts[1],
                end: parts[2],
            })
        }

        ActivitySet(activities)
    }
}
