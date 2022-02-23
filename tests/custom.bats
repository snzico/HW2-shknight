load harness

@test "custom-1" {
  check 'if -3 <= -3 then x := 8 else y := 6' '{x → 8}'
}

@test "custom-2" {
  check 'if ( ¬ ( false ) ) then x := ( 6 % 4 )  else r9 := 6' '{x → 2}'
}

@test "custom-3" {
  check 'if (7 % 3) < 4 then g := 1 else e := 9' '{e → 9}'
}

@test "custom-4" {
  check 'if true ∨ (1 >= 0) then p := t else p := t + 16' '{p → 0}'
}

@test "custom-5" {
  check 'm := 6 ; n := 7 ; while ¬ ( m >= n ) do { if m < n then a := a + ( b % a ) else a := a + ( 16 - b )' '{m → 7}'
}
