extern crate regex;

// use regex::{Captures, Regex};
use regex::{Regex};

use crate::types::MalErr::ErrString;
use crate::types::MalVal::{
  Nil, Bool, Int,
  String as MalString, Symbol,
  List, Vector,
};
use crate::types::{
  error, hash_map,
  MalVal, MalErr,
  MalRet, MalArgs,
};

#[derive(Debug, Clone)]
struct Reader {
  tokens: Vec<String>,
  position: usize,
}

impl Reader {
  fn new(tokens: Vec<String>) -> Result<Reader, MalErr> {
    if tokens.len() == 0 {
      return Err(ErrString("empty tokens".to_string()))
    }
    Ok(Reader {
      tokens: tokens,
      position: 0,
    })
  }
  fn next(&mut self) -> Result<String, MalErr> {
    self.position = self.position + 1;
    Ok(self
      .tokens
      .get(self.position - 1)
      .ok_or(ErrString("underflow".to_string()))?
      .to_string()
    )
  }
  fn peek(&self) -> Result<String, MalErr> {
    Ok(self
      .tokens
      .get(self.position)
      .ok_or(ErrString("underflow".to_string()))?
      .to_string()
    )
  }
}

fn tokenize(str: &str) -> Vec<String> {
  lazy_static! {
    static ref TOKEN_RE: Regex = Regex::new(
      r#"[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"#
    )
    .unwrap();
  }

  let mut res = vec![];
  for cap in TOKEN_RE.captures_iter(str) {
    if cap[1].starts_with(";") {
      continue
    }
    res.push(String::from(&cap[1]));
  }
  res
}

fn read_atom(reader: &mut Reader) -> MalRet {
  lazy_static! {
    static ref INT_RE: Regex = Regex::new(r"^-?[0-9]+$").unwrap();
    static ref STRING_RE: Regex = Regex::new(r#""(:?\\.|[^\\"])*""#).unwrap();
  }

  let token = reader.next()?;
  match &token[..] {
    "nil" => Ok(Nil),
    "true" => Ok(Bool(true)),
    "false" => Ok(Bool(false)),
    _ => {
      if INT_RE.is_match(&token) {
        Ok(Int(token.parse().unwrap()))
      } else if STRING_RE.is_match(&token) {
        Ok(MalString(token.to_string()))
      } else if token.starts_with('"') {
        error("expected '\"', got EOF")
      } else if token.starts_with(':') {
        // keyword
        Ok(MalString(format!("\u{29e}{}", &token[1..])))
      } else {
        Ok(Symbol(token.to_string()))
      }
    }
  }
}

fn read_sequence(reader: &mut Reader, end: &str) -> Result<MalArgs, MalErr> {
  reader.next()?;

  let mut seq: Vec<MalVal> = vec![];
  loop {
    let token = match reader.peek() {
        Ok(t) => t,
        Err(_) => return Err(ErrString(format!("expected '{}', got EOF", end))),
    };
    if token == end {
      break
    }
    seq.push(read_form(reader)?);
  }
  reader.next()?;
  Ok(seq)
}

fn read_list(reader: &mut Reader) -> MalRet {
  Ok(List(read_sequence(reader, ")")?))
}

fn read_vector(reader: &mut Reader) -> MalRet {
  Ok(Vector(read_sequence(reader, "]")?))
}

fn read_hash_map(reader: &mut Reader) -> MalRet {
  hash_map(read_sequence(reader, "}")?)
}

fn read_form(reader: &mut Reader) -> MalRet {
  let token = reader.peek()?;

  match &token[..] {
    // comment
    ";" => {
      let _ = reader.next();
      Ok(Nil)
    },

    // ?
    "\'" => {
      let _ = reader.next();
      Ok(List(vec![Symbol("quote".to_string()), read_form(reader)?]))
    },
    "`" => {
      let _ = reader.next();
      Ok(List(vec![Symbol("quasiquote".to_string()), read_form(reader)?]))
    },
    "~" => {
      let _ = reader.next();
      Ok(List(vec![Symbol("unquote".to_string()), read_form(reader)?]))
    },
    "~@" => {
      let _ = reader.next();
      Ok(List(vec![Symbol("splice-unquote".to_string()), read_form(reader)?]))
    },
    // meta よくわからん
    // "^" => {
    //   let _ = reader.next();
    //   Ok(List(vec![Symbol("quote".to_string()), read_form(reader)?]))
    // },
    "@" => {
      let _ = reader.next();
      Ok(List(vec![Symbol("deref".to_string()), read_form(reader)?]))
    },

    // sequence
    "(" => read_list(reader),
    "[" => read_vector(reader),
    "{" => read_hash_map(reader),
    _ => read_atom(reader),
  }
}

pub fn read_str(line: String) -> MalRet {
  let tokens = tokenize(&line);
  // FIXME: remove debug code
  // println!("{:?}", &tokens);
  if tokens.len() == 0 {
    return error("no input")
  }
  let mut reader = Reader::new(tokens).unwrap();
  let ast = read_form(&mut reader);
  ast
}