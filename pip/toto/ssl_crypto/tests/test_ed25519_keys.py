#!/usr/bin/env/ python

"""
<Program Name>
  test_ed25519_keys.py

<Author> 
  Vladimir Diaz <vladimir.v.diaz@gmail.com> 

<Started>
  October 11, 2013. 

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test cases for test_ed25519_keys.py.
"""

# Help with Python 3 compatibility, where the print statement is a function, an
# implicit relative import is invalid, and the '/' operator performs true
# division.  Example:  print 'hello world' raises a 'SyntaxError' exception.
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest
import os
import logging

from ...ssl_commons import exceptions as ssl_commons__exceptions
from .. import formats as ssl_crypto__formats
from .. import ed25519_keys as ssl_crypto__ed25519_keys

logger = logging.getLogger('ssl_crypto__test_ed25519_keys')

public, private = ssl_crypto__ed25519_keys.generate_public_and_private()
FORMAT_ERROR_MSG = 'ssl_commons__exceptions.FormatError raised.  Check object\'s format.'


class TestEd25519_keys(unittest.TestCase):
  def setUp(self):
    pass


  def test_generate_public_and_private(self):
    pub, priv = ssl_crypto__ed25519_keys.generate_public_and_private()
    
    # Check format of 'pub' and 'priv'.
    self.assertEqual(True, ssl_crypto__formats.ED25519PUBLIC_SCHEMA.matches(pub))
    self.assertEqual(True, ssl_crypto__formats.ED25519SEED_SCHEMA.matches(priv))



  def test_create_signature(self):
    global public
    global private
    data = b'The quick brown fox jumps over the lazy dog'
    signature, method = ssl_crypto__ed25519_keys.create_signature(public, private, data)

    # Verify format of returned values.
    self.assertEqual(True,
                     ssl_crypto__formats.ED25519SIGNATURE_SCHEMA.matches(signature))
    
    self.assertEqual(True, ssl_crypto__formats.NAME_SCHEMA.matches(method))
    self.assertEqual('ed25519', method)

    # Check for improperly formatted argument.
    self.assertRaises(ssl_commons__exceptions.FormatError,
                      ssl_crypto__ed25519_keys.create_signature, 123, private, data)
    
    self.assertRaises(ssl_commons__exceptions.FormatError,
                      ssl_crypto__ed25519_keys.create_signature, public, 123, data)
   
    # Check for invalid 'data'.
    self.assertRaises(ssl_commons__exceptions.CryptoError,
                      ssl_crypto__ed25519_keys.create_signature, public, private, 123)


  def test_verify_signature(self):
    global public
    global private
    data = b'The quick brown fox jumps over the lazy dog'
    signature, method = ssl_crypto__ed25519_keys.create_signature(public, private, data)

    valid_signature = ssl_crypto__ed25519_keys.verify_signature(public, method, signature, data)
    self.assertEqual(True, valid_signature)
    
    # Test with 'pynacl'.
    valid_signature = ssl_crypto__ed25519_keys.verify_signature(public, method, signature, data,
                                               use_pynacl=True)
    self.assertEqual(True, valid_signature)
   
    # Test with 'pynacl', but a bad signature is provided.
    bad_signature = os.urandom(64)
    valid_signature = ssl_crypto__ed25519_keys.verify_signature(public, method, bad_signature,
                                               data, use_pynacl=True)
    self.assertEqual(False, valid_signature)
    


    # Check for improperly formatted arguments.
    self.assertRaises(ssl_commons__exceptions.FormatError, ssl_crypto__ed25519_keys.verify_signature, 123, method,
                                       signature, data)
    
    # Signature method improperly formatted.
    self.assertRaises(ssl_commons__exceptions.FormatError, ssl_crypto__ed25519_keys.verify_signature, public, 123,
                                       signature, data)
   
    # Invalid signature method.
    self.assertRaises(ssl_commons__exceptions.UnknownMethodError, ssl_crypto__ed25519_keys.verify_signature, public,
                                       'unsupported_method', signature, data)
   
    # Signature not a string.
    self.assertRaises(ssl_commons__exceptions.FormatError, ssl_crypto__ed25519_keys.verify_signature, public, method,
                                       123, data)
   
    # Invalid signature length, which must be exactly 64 bytes..
    self.assertRaises(ssl_commons__exceptions.FormatError, ssl_crypto__ed25519_keys.verify_signature, public, method,
                                       'bad_signature', data)
    
    # Check for invalid signature and data.
    # Mismatched data.
    self.assertEqual(False, ssl_crypto__ed25519_keys.verify_signature(public, method,
                                                     signature, '123'))
   
    # Mismatched signature.
    bad_signature = b'a'*64 
    self.assertEqual(False, ssl_crypto__ed25519_keys.verify_signature(public, method,
                                                     bad_signature, data))
    
    # Generated signature created with different data.
    new_signature, method = ssl_crypto__ed25519_keys.create_signature(public, private, 
                                                     b'mismatched data')
    
    self.assertEqual(False, ssl_crypto__ed25519_keys.verify_signature(public, method,
                                                     new_signature, data))



# Run the unit tests.
if __name__ == '__main__':
  unittest.main()
