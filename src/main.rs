mod machine_turing;
mod cellular_automata;

fn test_mt() {
    use machine_turing::*;
    use std::collections::HashMap;

    let ribbon = Ribbon::from(vec!["0","1","1","1"]);
    let states = vec![
        State::from("start",false),
        State::from("accept",true),
        State::from("reject",false),
        State::from("right",false),
        State::from("add",false)
    ];
    let init_state = String::from("start");
    let mut transitions: HashMap<String,Vec<Transition>> = HashMap::new();
    transitions.insert(String::from("start"), vec![
        Transition::from("", "", MoveTo::Stay, "reject"),
        Transition::from("0","0",MoveTo::Right,"right")
    ]);
    transitions.insert(String::from("right"), vec![
        Transition::from("1","1",MoveTo::Right,"right"),
        Transition::from("0","0",MoveTo::Right,"right"),
        Transition::from("", "",MoveTo::Left, "add")
    ]);
    transitions.insert(String::from("add"), vec![
        Transition::from("0","1",MoveTo::Stay,"accept"),
        Transition::from("1","0",MoveTo::Left,"add"),
        Transition::from("","1",MoveTo::Stay,"accept")
    ]);
    let mut mt = MachineTuring::new(Configuration::new(ribbon, states, init_state, transitions));
    match mt.run_with_limit(10) {
        Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
        Err(_) => println!("Error when run the MT :\n{:?}",mt.configuration.get_ribbon())
    }
}

fn main() {
    test_mt();
}
