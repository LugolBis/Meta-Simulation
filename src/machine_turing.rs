use std::collections::HashMap;
use std::fs;

#[derive(Debug, Clone)]
pub enum MoveTo {
    Right,
    Left,
    Stay
}

#[derive(Debug,Clone)]
pub struct Ribbon {
    head: usize,
    value: Vec<String>
}

#[derive(Debug, Clone)]
pub struct Transition {
    read: String,
    write: String,
    movement: MoveTo,
    futur_state: String
}

#[derive(Debug)]
pub struct Configuration {
    ribbon: Ribbon, // That modelize the ribbon of the Machine of Turing
    current_state: String,
}

#[derive(Debug)]
pub struct MachineTuring {
    pub configuration: Configuration,
    pub final_states: Vec<String>,
    pub transitions: HashMap<String,Vec<Transition>>,
    pub step: u64
}

impl Ribbon {
    pub fn from(input: Vec<&str>) -> Self {
        Self { head: 0usize, value: input.iter().map(|c| String::from(*c)).collect() }
    }

    pub fn get(&self) -> &String {
        &self.value[self.head]
    }

    pub fn set(&mut self, new_value: String) {
        self.value[self.head] = new_value;
    }

    pub fn left(&mut self) {
        if self.head == 0 { todo!(); }
        else { self.head -= 1; }
    }

    pub fn right(&mut self) {
        if self.head == self.value.len()-1 { self.value.push(String::from("_")); self.head += 1; }
        else { self.head += 1; }
    }
}

impl Transition {
    pub fn from(read:&str,write:&str,movement:MoveTo,futur_state:&str) -> Self {
        Self { read: String::from(read), write: String::from(write), movement: movement, futur_state: String::from(futur_state) }
    }
}

impl Configuration {
    pub  fn new(ribbon: Ribbon,current_state: String) -> Self {
        Self { ribbon: ribbon, current_state: current_state }
    }

    pub fn get_ribbon(&self) -> &Ribbon {
        &self.ribbon
    }
    
    pub fn get_mut_ribbon(&mut self) -> &mut Ribbon {
        &mut self.ribbon
    }

    pub fn get_current_state(&self) -> String {
        String::from(&self.current_state)
    }

    pub fn update(&mut self, transitions:Vec<Transition>) -> Result<(), ()> {   
        let ribbon = self.get_mut_ribbon();
        for transition in transitions {
            if transition.read == *ribbon.get() {
                ribbon.set(transition.write.clone());
                match transition.movement {
                    MoveTo::Left => ribbon.left(),
                    MoveTo::Right => ribbon.right(),
                    MoveTo::Stay => {}
                }
                self.current_state = transition.futur_state;
                return Ok(());
            }
        }
        Err(())
    }
}

impl MachineTuring {
    pub fn new(configuration:Configuration, final_states:Vec<&str>, transitions:HashMap<String,Vec<Transition>>) -> Self {
        Self { configuration: configuration, final_states: final_states.iter().map(|c| c.to_string()).collect(), transitions: transitions, step: 0u64 }
    }

    pub fn from_file(file_path:&str) -> Result<Self, String> {
        //! Read a Turing Machine who is stored in a specific format in a file.<br>
        //! The format is the following :<br>
        //! **First line** : The initializing state<br>
        //! **Second line** : The finals states separated by ',' like : *q1*,*q2*,*q3*<br>
        //! **Fird line** : The ribbon in input where each bow is separated by ',' like : *0*,*1*,*1*,*0*,*1*<br>
        //! **The other lines** : Transitions formated like that : state_start,read,state_end,write,movement<br>
        //! **Note** : The movements are '<' (left), '>' right, '-' (stay)
        let lines = fs::read_to_string(file_path)
            .map_err(|error| format!("{}",error))?;
        let lines = lines.split("\n").filter(|l| *l!="").collect::<Vec<&str>>();
        let current_state = String::from(lines[0usize]);
        let final_states = lines[1usize].split(",").map(|c| String::from(c.trim())).collect::<Vec<String>>();
        let ribbon = Ribbon::from(lines[2usize].split(",").collect::<Vec<&str>>());
        let mut transitions: HashMap<String,Vec<Transition>> = HashMap::new();
        for index in 3..lines.len() {
            let new_trans = lines[index].split(",").collect::<Vec<&str>>();
            let state = new_trans[0];
            match new_trans[4usize] {
                "-" => {
                    match transitions.get_mut(state) {
                        Some(vector) => {vector.push(Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Stay, new_trans[2]));},
                        None => {transitions.insert(String::from(new_trans[0]), vec![Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Stay, new_trans[2])]);}
                    }
                }
                "<" => {
                    match transitions.get_mut(state) {
                        Some(vector) => {vector.push(Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Left, new_trans[2]));},
                        None => {transitions.insert(String::from(new_trans[0]), vec![Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Left, new_trans[2])]);}
                    }
                }
                ">" => {
                    match transitions.get_mut(state) {
                        Some(vector) => {vector.push(Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Right, new_trans[2]));},
                        None => {transitions.insert(String::from(new_trans[0]), vec![Transition::from(new_trans[1], new_trans[3],
                            MoveTo::Right, new_trans[2])]);}
                    }
                }
                error => {return Err(format!("Error : Unknow symbol for the movement '{}'",error))}
            }
        };
        Ok(Self { configuration: Configuration::new(ribbon,current_state), final_states: final_states, transitions: transitions, step: 0u64 })
    }

    pub fn get_transitions(&self) -> Option<Vec<Transition>> {
        match self.transitions.get(&self.configuration.get_current_state()) {
            Some(vector) => Some(vector.clone()),
            None => None
        }
    }

    pub fn run(&mut self) -> Result<(),()> {
        let mut active = true;
        while active {
            match self.get_transitions() {
                Some(transitions) => {
                    if let Err(_) = self.configuration.update(transitions).clone() {
                        active = false;
                    }
                }
                None => active = false
            }
            
        }
        self.check_final_state()
    }

    pub fn run_with_limit(&mut self, limit:u64) -> Result<(),()> {
        let mut active = true;
        while active && self.step<limit {
            match self.get_transitions() {
                Some(transitions) => {
                    if let Err(_) = self.configuration.update(transitions).clone() {
                        active = false;
                    }
                }
                None => active = false
            }
            
        }
        self.check_final_state()
    }

    pub fn check_final_state(&self) -> Result<(),()> {
        let final_states = self.final_states.clone();
        for state in final_states {
            if state == self.configuration.current_state {
                return Ok(());
            }
        }
        Err(())
    }
}

pub fn load_and_run_config(machine_turing:&mut MachineTuring,configuration:Configuration,limit:u64) -> Result<(), ()> {
    //! This function load a Configuration in a MachineTuring and run it with a specified limit.
    machine_turing.configuration = configuration;
    machine_turing.run_with_limit(limit)
}

#[cfg(test)]
mod tests {
    use crate::machine_turing::*; 

    fn create_mt() -> MachineTuring {
        let ribbon = Ribbon::from(vec!["0","1","1","1"]);
        let final_states = vec!["start","accept","reject","right","add"];
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
        MachineTuring::new(Configuration::new(ribbon,  init_state),final_states, transitions)
    }

    #[test]
    fn test_run() {
        let mut mt = create_mt();
        match mt.run() {
            Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
            Err(_) => println!("Error when run the MT :\n{:?}",mt.configuration.get_ribbon())
        }
    }

    #[test]
    fn test_run_limit() {
        let mut mt = create_mt();
        match mt.run_with_limit(10) {
            Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
            Err(_) => println!("Error when run the MT :\n{:?}",mt.configuration.get_ribbon())
        }
    }

    #[test]
    fn test_run_script() {
        match MachineTuring::from_file("test.txt") {
            Ok(mut mt) => {
                match mt.run_with_limit(10) {
                    Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
                    Err(error) => panic!("Error when run the MT :\n{:?}\n{:?}",mt.configuration.get_ribbon(),error)
                }
            },
            Err(error) => panic!("Error when try to load the MT from a script :\n{:?}",error)
        }
    }
}