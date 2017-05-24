auto file, fname, i, address, size, x;
address = 0xF770B000;
size = 0x001D74;
fname = "dump_mem.bin";
file = fopen(fname, "wb");
for (i=0; i<size; i++, address++)
{
 x = DbgByte(address);
 fputc(x, file);
}
fclose(file);
