from setup.initialize import config
i = float(config.get("SR830", "signal_input"))
i= f'{i:.3f}'
print(f'{i:.3f}')