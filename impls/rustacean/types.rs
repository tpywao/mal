use std::any::type_name;
use std::collections::HashMap as RustHashMap;
use itertools::Itertools;


use crate::types::MalVal::HashMap;
use crate::types::MalErr::{ErrString};


#[derive(Debug, Clone)]
pub enum MalVal {
  Nil,
  Bool(bool),
  Int(i64),
  String(String),
  Symbol(String),
  List(Vec<MalVal>),
  Vector(Vec<MalVal>),
  // malでは文字列キーしか実装しない
  HashMap(RustHashMap<String, MalVal>),
}


#[derive(Debug)]
pub enum MalErr {
  ErrString(String),
}

pub type MalRet = Result<MalVal, MalErr>;
pub type MalArgs = Vec<MalVal>;


// type utility functions

pub fn type_of<T>(_: T) -> &'static str {
  type_name::<T>()
}

pub fn error(s: &str) -> MalRet {
  Err(ErrString(s.to_string()))
}

pub fn hash_map(kvs: Vec<MalVal>) -> MalRet {
  // 2回collectを使ってるの微妙...
  let hm = kvs.iter().tuples().map(|(k, v)| {
    match k {
      MalVal::String(k) => Ok((k.to_string(), v.clone())),
      k => Err(ErrString(format!(
        "hash key expected MalVal::String, got {:?}({})", k, type_of(k)))),
    }
  })
  // vecに結果を集める。Errがあれば?でreturnされる
  .collect::<Result<Vec<_>, _>>()?
  // もう一度iterに変換してHashMapに集める
  .into_iter().collect::<RustHashMap<_, _>>();
  Ok(HashMap(hm))

  // insertを使った例 (元コード mal/impls/rust/types.rs#hash_map)
  // let mut hm = RustHashMap::new();
  // for (k, v) in kvs.iter().tuples() {
  //   match k {
  //     MalVal::String(k) => {
  //       hm.insert(k.to_string(), v.clone());
  //     },
  //     _ => return error("hash key is not String"),
  //   }
  // }
  // Ok(HashMap(hm))
}
