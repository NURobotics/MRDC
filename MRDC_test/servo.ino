void release_wall() {
  if(wall_state == 1) { //wall is up, pull it down
    wall.write(0);
    wall_state = 0;
  } else {
    wall.write(initial_pos);
    wall_state = 1;
  }
  
}

