=============================
DRFMultiStepForm
=============================

Your project description goes here

Documentation
-------------

The full documentation is at https://DRFMultiStepForm.readthedocs.io.

Quickstart
----------

Install DRFMultiStepForm::

    pip install drf-multistep-form

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'form,
        ...
    )

Add DRFMultiStepForm's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        url('form/', include(form.urls)),
        ...
    ]