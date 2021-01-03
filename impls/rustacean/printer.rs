use crate::types::MalVal;
use crate::types::MalVal::{
  Nil, Bool, Int,
  String as MalString, Symbol,
  List, Vector, HashMap,
};

impl MalVal {
  pub fn pr_str(&self) -> String {
    match self {
      Nil => "nil".to_string(),
      Bool(true) => "true".to_string(),
      Bool(false) => "false".to_string(),
      Int(i) => i.to_string(),
      MalString(s) => {
        if s.starts_with("\u{29e}") {
          format!(":{}", &s[2..])
        } else {
          s.clone()
        }
      },
      Symbol(s) => s.clone(),
      List(l) => pr_sequence(l, "(", ")"),
      Vector(v) => pr_sequence(v, "[", "]"),
      HashMap(hm) => {
        let l: Vec<MalVal> = hm
          .iter()
          .flat_map(|(k, v)| vec![MalString(k.to_string()), v.clone()])
          .collect();
        pr_sequence(&l, "{", "}")
      },
    }
  }
}

fn pr_sequence(
  sequence: &Vec<MalVal>,
  start: &str,
  end: &str,
) -> String {
  let strs: Vec<String> = sequence.iter().map(|val| val.pr_str()).collect();
  format!("{}{}{}", start, strs.join(" "), end)
}
