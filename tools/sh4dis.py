import struct,sys
BASE=0x8c010000
def dis(d,pc_off):
    op=struct.unpack_from('<H',d,pc_off)[0];pc=BASE+pc_off
    n=(op>>8)&15;m=(op>>4)&15;i8=op&0xff;s8=i8-256 if i8&0x80 else i8;d4=op&15
    t=op>>12
    def lit(sz):
        a=(pc&~3 if sz==4 else pc)+4+i8*sz;o=a-BASE
        v=struct.unpack_from('<I' if sz==4 else '<h',d,o)[0] if 0<=o<len(d) else 0
        return a,v
    if t==0xE: return f'mov #{s8},r{n}'
    if t==0x9: a,v=lit(2);return f'mov.w @({a:x}),r{n}  ; ={v:#x}'
    if t==0xD: a,v=lit(4);return f'mov.l @({a:x}),r{n}  ; ={v:#x}'
    if t==0x7: return f'add #{s8},r{n}'
    if t==0xA: return f'bra {pc+4+((op&0xfff)-(0x1000 if op&0x800 else 0))*2:x}'
    if t==0xB: return f'bsr {pc+4+((op&0xfff)-(0x1000 if op&0x800 else 0))*2:x}'
    if t==0x1: return f'mov.l r{m},@({d4*4},r{n})'
    if t==0x5: return f'mov.l @({d4*4},r{m}),r{n}'
    if t==0x6:
        x=['mov.b @r{m},r{n}','mov.w @r{m},r{n}','mov.l @r{m},r{n}','mov r{m},r{n}','mov.b @r{m}+,r{n}','mov.w @r{m}+,r{n}','mov.l @r{m}+,r{n}','not r{m},r{n}','swap.b r{m},r{n}','swap.w r{m},r{n}','negc r{m},r{n}','neg r{m},r{n}','extu.b r{m},r{n}','extu.w r{m},r{n}','exts.b r{m},r{n}','exts.w r{m},r{n}'][d4]
        return x.format(m=m,n=n)
    if t==0x2:
        x=['mov.b r{m},@r{n}','mov.w r{m},@r{n}','mov.l r{m},@r{n}','?','mov.b r{m},@-r{n}','mov.w r{m},@-r{n}','mov.l r{m},@-r{n}','div0s','tst r{m},r{n}','and r{m},r{n}','xor r{m},r{n}','or r{m},r{n}','cmp/str','xtrct','mulu.w r{m},r{n}','muls.w r{m},r{n}'][d4]
        return x.format(m=m,n=n)
    if t==0x3:
        x=['cmp/eq r{m},r{n}','?','cmp/hs r{m},r{n}','cmp/ge r{m},r{n}','div1','dmulu','cmp/hi r{m},r{n}','cmp/gt r{m},r{n}','sub r{m},r{n}','?','subc','subv','add r{m},r{n}','dmuls','addc','addv'][d4]
        return x.format(m=m,n=n)
    if t==0x4:
        low=op&0xff
        tab={0x0b:'jsr @r{n}',0x2b:'jmp @r{n}',0x00:'shll r{n}',0x01:'shlr r{n}',0x08:'shll2 r{n}',0x09:'shlr2 r{n}',0x18:'shll8 r{n}',0x19:'shlr8 r{n}',0x28:'shll16 r{n}',0x29:'shlr16 r{n}',0x22:'sts.l pr,@-r{n}',0x26:'lds.l @r{n}+,pr',0x10:'dt r{n}',0x15:'cmp/pl r{n}',0x11:'cmp/pz r{n}',0x20:'shal r{n}',0x21:'shar r{n}'}
        if low in tab: return tab[low].format(n=n)
        if d4==0xc: return f'shad r{m},r{n}'
        if d4==0xd: return f'shld r{m},r{n}'
        return f'op4 {op:04x}'
    if t==0x0:
        if op==0x000b: return 'rts'
        if op==0x0009: return 'nop'
        if d4==7: return f'mul.l r{m},r{n}'
        if d4==0xc: return f'mov.b @(r0,r{m}),r{n}'
        if d4==0xd: return f'mov.w @(r0,r{m}),r{n}'
        if d4==0xe: return f'mov.l @(r0,r{m}),r{n}'
        if d4==4: return f'mov.b r{m},@(r0,r{n})'
        if d4==5: return f'mov.w r{m},@(r0,r{n})'
        if d4==6: return f'mov.l r{m},@(r0,r{n})'
        if op&0xff==0x1a: return f'sts macl,r{n}'
        if op&0xff==0x29: return f'movt r{n}'
        return f'op0 {op:04x}'
    if t==0x8:
        sub=n;tgt=pc+4+s8*2
        x={0:f'mov.b r0,@({d4},r{m})',1:f'mov.w r0,@({d4*2},r{m})',4:f'mov.b @({d4},r{m}),r0',5:f'mov.w @({d4*2},r{m}),r0',8:f'cmp/eq #{s8},r0',9:f'bt {tgt:x}',0xb:f'bf {tgt:x}',0xd:f'bt/s {tgt:x}',0xf:f'bf/s {tgt:x}'}
        return x.get(sub,f'op8 {op:04x}')
    if t==0xC:
        sub=n;x={7:f'mova @({(pc&~3)+4+i8*4:x}),r0',8:f'tst #{i8},r0',9:f'and #{i8},r0',0xb:f'or #{i8},r0',0xa:f'xor #{i8},r0'}
        return x.get(sub,f'opC {op:04x}')
    return f'{op:04x}'
if __name__=='__main__':
    d=open(sys.argv[1],'rb').read();s=int(sys.argv[2],16);e=int(sys.argv[3],16)
    for o in range(s,e,2): print(f'{BASE+o:08x} {o:06x}: {dis(d,o)}')
