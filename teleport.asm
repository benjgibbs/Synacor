;
; assemble and link with:
; $ /usr/local/bin/nasm -f macho64 teleport.asm && ld -macosx_version_min 10.10.0 -lSystem -o teleport teleport.o                                                               <<<

section .text
global _main
extern _printf

_main:
	; mov rdi,str
	; add esp,1
  ; mov rsi,0xDEADBEEF
  ; call _printf
  ; ret strlen

section .data
	str:
		db `test\n`
		 ;db `Register = %08X\n`
	strlen equ $ - str
