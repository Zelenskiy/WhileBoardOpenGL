program hello;
{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads
  {$ENDIF}{$ENDIF}
  ;

begin
  writeln('Hello');
end.

