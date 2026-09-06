import subprocess,sys
mods=['experiments.verify_across_bases','experiments.verify_across_pairs','experiments.verify_decimal_constant','experiments.verify_digit_asymptotics','experiments.discrepancy_diagnostics']
for mod in mods:
    print('RUN',mod,flush=True)
    subprocess.run([sys.executable,'-m',mod],check=True)
