%professions list
professions([smith,baker,carpenter,tailor]).


query([Smith,Baker,Carpenter,Tailor],[Son_Smith,Son_Baker,Son_Carpenter,Son_Tailor]):-
      professions(L),

      % name != profession
      member(Smith,L), not(Smith = smith),
      member(Baker,L), not(Baker = baker),
      member(Carpenter,L), not(Carpenter = carpenter),
      member(Tailor,L), not(Tailor = tailor),

      % name!= sons profession
      member(Son_Smith,L), not(Son_Smith=smith),	
      member(Son_Baker,L), not(Son_Baker=baker),
      member(Son_Carpenter,L), not(Son_Carpenter=carpenter),
      member(Son_Tailor,L), not(Son_Tailor=tailor),

      % fathers profession != sons profession
      member(Son_Smith,L), not(Son_Smith = Smith),	
      member(Son_Baker,L), not(Son_Baker = Baker),
      member(Son_Carpenter,L), not(Son_Carpenter = Carpenter),
      member(Son_Tailor,L), not(Son_Tailor = Tailor),
      
      % baker same profession as carpenters son
      Baker = Son_Carpenter, 

      % smiths son is baker
      Son_Smith = baker.

% function for print answer
solve():-
      query(Parents, Sons),
      write("Parents = "), write(Parents), nl,
      write("Sons = "), write(Sons), nl.