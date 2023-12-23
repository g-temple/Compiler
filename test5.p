program test5:
  a := 10
  b := 5

  if a = b:
    c := a
  else:
    if a > b:
      c := a
    else:
      c := b
    end
  end
  
  print c
end