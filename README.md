<h1 align="center">
    <b>WORK IN PROGRESS</b>
</h1>

# The AVERT Volcano Data API
The AVERT Volcano Data API provides HTTP-based access to the archive of volcano imagery collected as part of the [AVERT project](https://vulcan1.ldeo.columbia.edu). In future, it will also provide a basis for serving up standard plots of other time series data collected as part of the project e.g. daily helicorder/drum plots of seismic data.

## Installation
The API can be installed by cloning this repository and running `pip install .` in the source directory. It is not currently registered on the Python Package Index (nor is there any plan to do so in the near future).

Once installed, the API is configured with a pair of Dotenv files: `.env`, which contains PRIVATE information; and `.flaskenv`, which contains PUBLIC information. Edit the examples accordingly and add copies to the `avert_api` directory, then reinstall the package. Make sure the contents of the `.env` file is never commited to a remote repository, or placed somewhere it could be accessed.

## Futures
The database model is not finalised and will likely see some alteration to fully specify the data and related metadata.

Add the option to run a containerised version of the API, for deployment on cloud platforms.

## Contact
You can contact us directly at: avert-system [ at ] proton.me

Any additional comments/questions can be directed to:
* **Conor Bacon** - cbacon [ at ] ldeo.columbia.edu

## License
This package is written and maintained by the AVERT System Team, Copyright AVERT System Team 2023. It is distributed under the GPLv3 License. Please see the [LICENSE](LICENSE) file for a complete description of the rights and freedoms that this provides the user.
