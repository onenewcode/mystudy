fn main() {
    let data=[0; 0x2000];
    
    println!("{}",data.as_ptr() as usize+4096 * 2);
}
