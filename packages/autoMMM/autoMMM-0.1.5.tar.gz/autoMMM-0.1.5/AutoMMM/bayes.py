import numpy as np
import pymc as pm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


class VARModel:
    def __init__(
        self,
        n_lags: int,
        n_eqs: int,
        df: pd.DataFrame,
        priors: dict,
        exog_df: pd.DataFrame = None,
        mv_norm: bool = True,
        prior_checks: bool = True,
    ):
        """
        VARModel class constructor.

        Args:
            n_lags: The number of lags to include in the model.
            n_eqs: The number of equations in the VAR model.
            df: A pandas DataFrame containing the time series data.
            priors: A dictionary containing the prior distributions for model parameters.
            exog_df: An optional pandas DataFrame containing exogenous variables.
            mv_norm: A boolean indicating whether to use a multivariate normal distribution for the errors.
            prior_checks: A boolean indicating whether to perform prior checks.
        """
        self.n_lags = n_lags
        self.n_eqs = n_eqs
        self.df = df
        self.priors = priors
        self.mv_norm = mv_norm
        self.prior_checks = prior_checks

        if exog_df is not None:
            self.exog_df = exog_df.iloc[n_lags:]
        else:
            self.exog_df = None

        self.coords = {
            "lags": np.arange(self.n_lags) + 1,
            "equations": self.df.columns.tolist(),
            "cross_vars": self.df.columns.tolist(),
            "time": [x for x in self.df.index[self.n_lags:]],
        }
        if exog_df is not None:
            self.coords["exog_vars"] = self.exog_df.columns.tolist()

        self.model = None
        self.idata = None

    def calc_ar_step(
        self,
        lag_coefs,
        n_eqs: int,
        n_lags: int,
        df: pd.DataFrame,
        exog_coefs=None,
    ):
        """
        Calculate AR step given lag coefficients and data.

        Args:
            lag_coefs: The lag coefficients.
            n_eqs: The number of equations in the VAR model.
            n_lags: The number of lags to include in the model.
            df: A pandas DataFrame containing the time series data.
            exog_coefs: Optional coefficients for exogenous variables.

        Returns:
            beta: The calculated AR step.
        """
        if self.exog_df is not None:
            beta = pm.math.stack(
                [
                    pm.math.sum(
                        [
                            pm.math.sum(lag_coefs[j, i] * df.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                            for i in range(n_lags)
                        ],
                        axis=0,
                    )
                    + pm.math.dot(self.exog_df.values, exog_coefs[j])
                    for j in range(n_eqs)
                ],
                axis=-1,
            )

        else:
            beta = pm.math.stack(
                [
                    pm.math.sum(
                        [
                            pm.math.sum(lag_coefs[j, i] * df.values[n_lags - (i + 1) : -(i + 1)], axis=-1)
                            for i in range(n_lags)
                        ],
                        axis=0,
                    )
                    for j in range(n_eqs)
                ],
                axis=-1,
            )

        return beta

    def fit(self, draws=2000, tune=1000, target_accept=0.9, random_seed=None, callback=None):
        """
        Fit the VAR model.

        Args:
            draws: The number of posterior samples to draw.
            tune: The number of tuning samples.
            target_accept: The target acceptance rate for the MCMC sampler.
            random_seed: Optional random seed for reproducibility.

        Returns:
            idata: InferenceData object containing posterior samples and predictions.
        """
        with pm.Model(coords=self.coords) as self.model:
            # VAR coefficients
            lag_coefs = pm.Normal(
                "lag_coefs",
                mu=self.priors["lag_coefs"]["mu"],
                sigma=self.priors["lag_coefs"]["sigma"],
                dims=["equations", "lags", "cross_vars"],
            )
            alpha = pm.Normal(
                "alpha", mu=self.priors["alpha"]["mu"], sigma=self.priors["alpha"]["sigma"], dims=("equations",)
            )

            # Exogenous coefficients
            if self.exog_df is not None:
                exog_coefs = pm.Normal(
                    "exog_coefs",
                    mu=self.priors["coefs"]["mu"],
                    sigma=self.priors["coefs"]["sigma"],
                    dims=["equations", "exog_vars"],
                )
            else:
                exog_coefs = None

            betaX = self.calc_ar_step(lag_coefs, self.n_eqs, self.n_lags, self.df, exog_coefs=exog_coefs)
            data_obs = pm.Data("data_obs", self.df.values[self.n_lags:], dims=["time", "equations"], mutable=True)

            betaX = pm.Deterministic(
                "betaX",
                betaX,
                dims=[
                    "time",
                    "equations"
                ],
            )

            mean = alpha + betaX

            if self.mv_norm:
                n = self.df.shape[1]
                noise_chol, _, _ = pm.LKJCholeskyCov(
                    "noise_chol",
                    eta=self.priors["noise_chol"]["eta"],
                    n=n,
                    sd_dist=pm.HalfNormal.dist(sigma=self.priors["noise_chol"]["sigma"]),
                )
                obs = pm.MvNormal(
                    "obs", mu=mean, chol=noise_chol, observed=data_obs, dims=["time", "equations"]
                )
            else:
                sigma = pm.HalfNormal("noise", sigma=self.priors["noise"]["sigma"], dims=["equations"])
                obs = pm.Normal(
                    "obs", mu=mean, sigma=sigma, observed=data_obs, dims=["time", "equations"]
                )

            if self.prior_checks:
                self.idata = pm.sample_prior_predictive()
                return self.idata
            else:
                self.idata = pm.sample(draws=draws, tune=tune, target_accept=target_accept, random_seed=random_seed, callback=callback)
                pm.sample_posterior_predictive(self.idata, extend_inferencedata=True, random_seed=random_seed)
                return self.idata

    def impulse_response_function(
        self,
        var_coef=None,
        num_periods=10,
        shock_var=0,
        shock_magnitude=1,
        cumsum=False,
        plot=True,
    ):
        """
        Compute the impulse response function (IRF) of the VAR model.

        Args:
            var_coef: Optional custom VAR coefficients.
            num_periods: The number of periods to compute the IRF for.
            shock_var: The index of the variable to shock.
            shock_magnitude: The magnitude of the shock.
            cumsum: A boolean indicating whether to compute the cumulative IRF.
            plot: A boolean indicating whether to plot the IRF.

        Returns:
            irf_df: A pandas DataFrame containing the IRF.
        """
        if var_coef is None:
            var_coef = self.idata.posterior["lag_coefs"].mean(dim=["chain", "draw"]).values.mean(1)

        p = var_coef.shape[0]  # number of variables in the VAR model
        irf = np.zeros((num_periods + 1, p))  # initialize array for impulse response function
        irf[0, shock_var] = shock_magnitude  # initial observation that shows the shock

        # create selection vector for the shock variable
        ej = np.zeros((p, 1))
        ej[shock_var] = shock_magnitude

        # compute impulse response function for each period
        for t in range(num_periods):
            if t == 0:
                irf[t + 1] = (var_coef @ ej).flatten()  # initial response
            else:
                irf[t + 1] = (var_coef @ irf[t].reshape(-1, 1)).flatten()  # subsequent responses

        # compute cumulative impulse response function, if desired
        if cumsum:
            irf = np.cumsum(irf, axis=0)

        irf_df = pd.DataFrame(irf, columns=self.df.columns)

        if plot:
            self.plot_irf(irf_df, cumsum=cumsum)

        return irf_df

    def plot_irf(self, irf, cumsum=False):
        """
        Plot the impulse response function (IRF).

        Args:
            irf: A pandas DataFrame containing the IRF.
            cumsum: A boolean indicating whether to plot the cumulative IRF.
        """
        fig, axs = plt.subplots(nrows=len(self.df.columns), ncols=1, sharex=True, figsize=(8, 8))
        fig.suptitle("Impulse Response Function", fontsize=14)

        for i, var in enumerate(self.df.columns):
            axs[i].plot(irf.index, irf[var])
            axs[i].axhline(y=0, color="k", linestyle="--", alpha=0.5)
            axs[i].set(title=f"Impulse Response of {var}", ylabel="Change")
            if cumsum:
                axs[i].set(title=f"Cumulative Impulse Response of {var}", ylabel="Cumulative Change")
            if i == len(self.df.columns) - 1:
                axs[i].set(xlabel="Periods")
        plt.tight_layout()
        plt.show()
        





