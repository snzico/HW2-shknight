load harness

@test "custom-1-lte" {
  check 'if -3 <= -3 then x := 8 else y := 6' '{x → 8}'
}

@test "custom-2-gt" {
  check 'i := 4 ; j := 1 ; while 0 < i do { i := i - j ; j := 2 * j }' '{i → -3, j → 8}'
}

@test "custom-3-gte" {
  check 'while ¬ ( x >= 3 ) do x := x + 1' '{x → 3}'
}

@test "custom-4-ternary" {
  check 'x := ( ( 16 % 13 ) <= 4 ) ? true : false' '{x → True}'
}

@test "custom-5-div" {
  check 'x := 2 ; y := x ; x := y / x' '{x → 1.0, y → 2}'
}

@test "custom-6-mod" {
  check 'x := 10 ; y := 3 ; while y > 0 do y := x % y ; x := x - 3' '{x → 7, y → 0}'
}
