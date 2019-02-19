use indexmap::IndexMap;
use std::cell::RefCell;
use std::collections::VecDeque;
use std::env::args;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader, ErrorKind};
use std::ops::Not;
use std::result::Result;

type Graph = IndexMap<String, RefCell<(Vec<String>, Option<Team>)>>;

#[derive(Copy, Eq, PartialEq, Clone, Debug)]
enum Team {
    Babyface,
    Heel,
}

impl Not for Team {
    type Output = Team;

    fn not(self) -> Team {
        match self {
            Team::Babyface => Team::Heel,
            Team::Heel => Team::Babyface,
        }
    }
}

fn pick_unassigned(graph: &Graph) -> &str {
    for (key, val) in graph {
        if val.borrow().1.is_none() {
            return &key;
        }
    }

    ""
}

fn main() -> Result<(), Box<dyn Error>> {
    let filename = match args().skip(1).next() {
        Some(name) => name,
        None => {
            eprintln!("You must pass a filename to load!");
            return Err(Box::new(io::Error::from(ErrorKind::InvalidInput)));
        }
    };

    let (data, first_key) = load_file(&filename)?;
    let mut is_possible = breadth_first_queue(&data, &first_key);
    while !data.values().all(|data| data.borrow().1.is_some()) {
        let chosen_start = pick_unassigned(&data);
        is_possible = breadth_first_queue(&data, chosen_start);
    }

    match is_possible {
        true => {
            println!("It's possible to make a bipartite graph!");
            let mut side_one = vec![];
            let mut side_two = vec![];
            for (key, val) in data {
                let team = val.borrow().1.unwrap();
                if team == Team::Babyface {
                    side_one.push(key);
                } else {
                    side_two.push(key);
                }
            }

            println!("Babyfaces: {}", side_one.join(" "));
            println!("Heel: {}", side_two.join(" "));
        }
        false => {
            println!("This combination is not possible.");
        }
    }

    Ok(())
}

fn breadth_first_queue(graph: &Graph, first_key: &str) -> bool {
    graph.get(first_key).unwrap().borrow_mut().1 = Some(Team::Babyface);

    let mut queue: VecDeque<String> = VecDeque::new();
    queue.push_back(first_key.to_string());

    while let Some(node) = queue.pop_front() {
        let node = graph.get(&node).unwrap();
        let node = node.borrow();
        for neighbor in node.0.iter() {
            let neighbor_string = neighbor;
            let mut neighbor = graph.get(neighbor_string).unwrap().borrow_mut();

            match neighbor.1 {
                None => {
                    queue.push_back(neighbor_string.to_string());
                    neighbor.1 = Some(!node.1.unwrap())
                }
                Some(team) if team == node.1.unwrap() => {
                    return false;
                }
                //The team exists and is already different
                Some(_) => {
                    continue;
                }
            };
        }

        // if let Entry::Occupied(node) = graph.entry(node.to_string()) {
        //     let node = node.get();
        //     for neighbor in &node.0 {
        //         let etry = unsafe { graph.get_mut_unchecked() };
        //         // .and_modify(|data| data.1 = Some(!node.1.unwrap()));

        //         match etry {
        //             Entry::Occupied(mut occupied) => {
        //                 let entry = occupied.get_mut();
        //                 match entry.1 {
        //                     None => Some(entry.1 = Some(!node.1.unwrap())),
        //                     Some(team) if team == node.1.unwrap() => {
        //                         return false;
        //                     }
        //                     //The team exists and is already different
        //                     Some(_) => {
        //                         continue;
        //                     }
        //                 };
        //             }
        //             Entry::Vacant(_) => {
        //                 return false;
        //             }
        //         }
        //     }
        // }
    }
    true
}

fn load_file(name: &str) -> Result<(Graph, String), Box<dyn Error>> {
    let mut results: Graph = IndexMap::new();
    let reader = BufReader::new(File::open(name)?);
    let mut line_iter = reader.lines().filter_map(Result::ok);
    let mut first_key = String::new();

    if let Some(participant_count) = line_iter.next() {
        let participant_count = participant_count.parse::<usize>()?;

        for i in 0..participant_count {
            let participant = match line_iter.next() {
                Some(participant) => participant,
                None => return Err(Box::new(io::Error::from(ErrorKind::InvalidData))),
            };

            if i == 0 {
                first_key.push_str(&participant);
            }

            // If value was some, there was already an item in the hashmap of this value
            if let Some(_) = results.insert(participant.to_string(), RefCell::new((vec![], None))) {
                return Err(Box::new(io::Error::from(ErrorKind::InvalidData)));
            };
        }
    }

    if let Some(connection_count) = line_iter.next() {
        let connection_count = connection_count.parse::<usize>()?;

        for _ in 0..connection_count {
            let connection = match line_iter.next() {
                Some(connection) => connection.split(" ").map(String::from).collect::<Vec<_>>(),
                None => return Err(Box::new(io::Error::from(ErrorKind::InvalidData))),
            };

            if connection.len() < 2 {
                return Err(Box::new(io::Error::from(ErrorKind::InvalidData)));
            }

            results
                .entry(connection[0].clone())
                .and_modify(|data| data.borrow_mut().0.push(connection[1].clone()));
            results
                .entry(connection[1].clone())
                .and_modify(|data| data.borrow_mut().0.push(connection[0].clone()));
        }
    }

    Ok((results, first_key))
}
